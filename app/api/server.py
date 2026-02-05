import os
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from starlette.responses import JSONResponse
from .model.classify_request_model import classify_request_model
from .model.domain_scan_request_model import domain_scan_request
from .model.ip_scan_request_model import IPScanRequest
from .model.parse_request_model import parse_request_model, parse_translation_model, parse_semantic, embed_index_model, RuntimeParsePayload
from .model.report_chat_request import ReportChatRequest
from .model.social_request_model import SocialScrapeRequest
from .nlp_manager.nlp_controller import nlp_controller
from .nlp_manager.nlp_enums import NLP_REQUEST_COMMANDS
from .ocr_manager.ocr_controller import ocr_controller
from .ocr_manager.ocr_emums import OCR_REQUEST_COMMANDS
from .runtime_parse_manager.runtime_parse_controller import runtime_parse_controller
from .runtime_parse_manager.runtime_parse_enum import RUNTIME_PARSE_REQUEST_COMMANDS
from .scan_manager.domain_scanner import domain_scanner
from .topic_manager.topic_classifier_controller import topic_classifier_controller
from .topic_manager.topic_classifier_enums import TOPIC_CLASSFIER_COMMANDS, TOPIC_CATEGORIES
from .social_manager.social_controller import social_controller
from .social_manager.social_enums import SOCIAL_REQUEST_COMMANDS
from . ioc_manager.ioc_controller import ioc_controller
from . ioc_manager.ioc_enums import IOC_REQUEST_COMMANDS
from typing import Optional
import tempfile
from pathlib import Path
from .scan_manager.scanners.ip_scanner import IPScanner
from contextlib import asynccontextmanager
import asyncio
import logging
import concurrent.futures

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class APIService:
    MAX_CONCURRENT_REQUESTS = 60

    def __init__(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_CONCURRENT_REQUESTS)
        loop = asyncio.get_event_loop()
        loop.set_default_executor(executor)

        self.scanner = domain_scanner()
        self.ip_scanner = IPScanner()
        self.scanner.wait_for_zap()

        self.app = FastAPI()
        self.semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_REQUESTS)
        self.waiting_requests = 0
        self.active_requests = 0
        self.waiting_lock = asyncio.Lock()

        self.m_runtime_parser = runtime_parse_controller()

        try:
            self.nlp_controller_instance = nlp_controller()
            self.topic_classifier_instance = topic_classifier_controller()
            self.ocr_controller_instance = ocr_controller()
            self.social_controller_instance = social_controller()
            self.ioc_controller_instance = ioc_controller()
        except Exception:
            raise RuntimeError("Controller initialization failed")



        self.app.add_api_route("/nlp/parse", self.nlp_parse, methods=["POST"])
        self.app.add_api_route("/nlp/parse/ai", self.nlp_parse_ai, methods=["POST"])
        self.app.add_api_route("/nlp/summarize/ai", self.nlp_summarise_ai, methods=["POST"])
        self.app.add_api_route("/nlp/chat/report", self.nlp_chat_report, methods=["POST"])
        self.app.add_api_route("/nlp/translate", self.nlp_translate, methods=["POST"])
        self.app.add_api_route("/topic_classifier/predict", self.topic_classifier_predict, methods=["POST"])
        self.app.add_api_route("/runtime/parse/user", self.runtime_parse_user, methods=["POST"])
        self.app.add_api_route("/runtime/parse/social", self.runtime_parse_social, methods=["POST"])
        self.app.add_api_route("/runtime/parse/cracked", self.runtime_parse_app, methods=["POST"])
        self.app.add_api_route("/runtime/parse/software", self.runtime_parse_software, methods=["POST"])
        self.app.add_api_route("/ocr/parse", self.ocr_parse, methods=["POST"])
        self.app.add_api_route("/debug/semaphore_status", self.semaphore_status, methods=["GET"])
        self.app.add_api_route("/urlscan/domain", self.urlscan_domain, methods=["POST"])
        self.app.add_api_route("/nlp/embed", self.nlp_embed, methods=["POST"])
        self.app.add_api_route("/nlp/init", self.nlp_init, methods=["POST"])
        self.app.add_api_route("/nlp/embed/index", self.nlp_embed_index, methods=["POST"])
        self.app.add_api_route("/social/scrape", self.social_scrape, methods=["POST"])
        self.app.add_api_route("/ioc/extract", self.ioc_extract, methods=["POST"])
        self.app.add_api_route("/urlscan/ip", self.urlscan_ip, methods=["POST"])


        loop.create_task(self.log_queue_size())

    @asynccontextmanager
    async def track_waiting(self, endpoint: str = "unknown"):
        async with self.waiting_lock:
            self.waiting_requests += 1
            logger.info(f"[START_WAIT] Request to {endpoint}. Waiting: {self.waiting_requests}")
        try:
            async with self.semaphore:
                async with self.waiting_lock:
                    self.waiting_requests -= 1
                    self.active_requests += 1
                    logger.info(f"[START] Request to {endpoint}. In Use: {self.active_requests}")
                yield
        finally:
            async with self.waiting_lock:
                self.active_requests -= 1
                logger.info(f"[END] Request to {endpoint}. In Use: {self.active_requests}")
                logger.info(
                    f"[CLOSED] Request to {endpoint}. Final state — Waiting: {self.waiting_requests}, In Use: {self.active_requests}"
                )

    async def semaphore_status(self):
        async with self.waiting_lock:
            return {
                "waiting_queue_size": self.waiting_requests,
                "active_slots": self.active_requests,
                "available_slots": max(0, self.MAX_CONCURRENT_REQUESTS - self.active_requests),
            }

    async def log_queue_size(self):
        while True:
            async with self.waiting_lock:
                logger.info(
                    f"[Queue Monitor] Waiting: {self.waiting_requests}, "
                    f"In Use: {self.active_requests}, "
                    f"Available: {max(0, self.MAX_CONCURRENT_REQUESTS - self.active_requests)}"
                )
            await asyncio.sleep(5)

    async def runtime_parse(self, payload: RuntimeParsePayload, command: int):
        async with self.track_waiting("/runtime/parse"):
            try:
                query = payload.text or {}
                if not query or all(value == "" for value in query.values()):
                    raise HTTPException(status_code=400, detail="Invalid query")

                state = self.m_runtime_parser.get_status(command, query)

                if state["status"] == "done":
                    return JSONResponse(content={"result": state.get("result", [])})

                if state["status"] == "pending":
                    return JSONResponse(content={
                        "status": "pending",
                        "progress": state.get("progress", 0),
                        "step": state.get("step", "")
                    })

                async def _run_with_timeout():
                    try:
                        await asyncio.wait_for(
                            asyncio.to_thread(self.m_runtime_parser.run_parse_job_sync, command, query),
                            timeout=1000
                        )
                    except asyncio.TimeoutError:
                        self.m_runtime_parser.clear_status(command, query)

                asyncio.create_task(_run_with_timeout())

                return JSONResponse(content={
                    "status": "pending",
                    "progress": 0,
                    "step": "queued"
                })

            except HTTPException:
                raise
            except Exception as exc:
                logger.error("Error in runtime parse", exc_info=True)
                raise HTTPException(status_code=500, detail="Server error") from exc

    async def runtime_parse_user(self, payload: RuntimeParsePayload):
        return await self.runtime_parse(payload, RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_USERNAME)

    async def runtime_parse_social(self, payload: RuntimeParsePayload):
        return await self.runtime_parse(payload, RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_SOCIAL)

    async def runtime_parse_app(self, payload: RuntimeParsePayload):
        return await self.runtime_parse(payload, RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_APP)

    async def runtime_parse_software(self, payload: RuntimeParsePayload):
        return await self.runtime_parse(payload, RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_SOFTWARE)

    async def process_request(self, request, command, controller, default_result, timeout=60, endpoint="unknown"):
        async with self.track_waiting(endpoint):
            try:
                result = await asyncio.wait_for(
                    controller(command, request),
                    timeout=timeout
                )
                return {"result": result}
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on {endpoint}")
                return {"result": default_result}
            except Exception:
                logger.error(f"Error in {endpoint}", exc_info=True)
                return {"result": default_result}

    async def nlp_parse(self, request: parse_request_model):
        logger.info("Received request at /nlp/parse")
        return await self.process_request(
            request=request.data,
            command=NLP_REQUEST_COMMANDS.S_PARSE,
            controller=self.nlp_controller_instance.invoke_trigger,
            default_result={},
            endpoint="/nlp/parse"
        )

    async def nlp_parse_ai(self, request: parse_request_model):
        logger.info("Received request at /nlp/parse/ai")
        return await self.process_request(
            request=request.data,
            command=NLP_REQUEST_COMMANDS.S_PARSE_AI,
            controller=self.nlp_controller_instance.invoke_trigger,
            default_result={},
            endpoint="/nlp/parse/ai"
        )

    async def nlp_summarise_ai(self, request: parse_request_model):
        logger.info("Received request at /nlp/summarize/ai")
        async with self.track_waiting("/nlp/summarize/ai"):
            try:
                result = await asyncio.wait_for(
                    self.nlp_controller_instance.invoke_trigger(
                        NLP_REQUEST_COMMANDS.S_SUMMARIZE_AI, request.data
                    ),
                    timeout=100
                )
                return {"result": result}
            except asyncio.TimeoutError:
                logger.warning("Summarization timeout")
                return {"result": {}}
            except Exception:
                logger.error("Summarization failed", exc_info=True)
                return {"result": {}}

    async def nlp_chat_report(self, model: ReportChatRequest):
        logger.info("Received request at /nlp/chat/report (local S_CHAT_AI)")
        return await self.process_request(
            request=model,
            command=NLP_REQUEST_COMMANDS.S_CHAT_AI,
            controller=self.nlp_controller_instance.invoke_trigger,
            default_result={},
            timeout=120,
            endpoint="/nlp/chat/report"
        )

    async def nlp_translate(self, model: parse_translation_model):
        logger.info("Received request at /nlp/nlp/translate (local S_TRANSLATE)")
        return await self.process_request(
            request=model,
            command=NLP_REQUEST_COMMANDS.S_TRANSLATE,
            controller=self.nlp_controller_instance.invoke_trigger,
            default_result={},
            timeout=120,
            endpoint="/nlp/translate"
        )

    async def topic_classifier_predict(self, request: classify_request_model):
        logger.info("Received request at /topic_classifier/predict")
        return await self.process_request(
            request=[request.title, request.description, request.keyword],
            command=TOPIC_CLASSFIER_COMMANDS.S_PREDICT_CLASSIFIER,
            controller=self.topic_classifier_instance.invoke_trigger,
            default_result=[TOPIC_CATEGORIES.S_THREAD_CATEGORY_GENERAL],
            endpoint="/topic_classifier/predict"
        )

    async def ocr_parse(self, file: UploadFile = File(...)):
        logger.info("Received request at /ocr/parse")
        content = await file.read()
        if len(content) > 50 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large")
        async with self.track_waiting("/ocr/parse"):
            try:
                result = await asyncio.wait_for(
                    self.ocr_controller_instance.invoke_trigger(OCR_REQUEST_COMMANDS.S_PARSE, [content]),
                    timeout=60
                )
                return {"text": result}
            except asyncio.TimeoutError as exc:
                logger.warning("OCR timeout")
                raise HTTPException(status_code=504, detail="Timeout") from exc
            except Exception as exc:
                logger.error("OCR error", exc_info=True)
                raise HTTPException(status_code=500, detail="Error processing file") from exc

    async def urlscan_domain(self, request: domain_scan_request):
        logger.info("Received request at /urlscan/domain")
        async with self.track_waiting("/urlscan/domain"):
            try:
                domain = request.domain.strip()
                if not domain:
                    raise HTTPException(status_code=400, detail="Domain required")

                state = self.scanner.get_scan_status(domain, request.scanType)

                if state["status"] == "done":
                    return {"result": state["result"]}

                if state["status"] == "pending":
                    return {
                        "status": "pending",
                        "progress": state.get("progress", 0),
                        "step": state.get("step", "")
                    }

                asyncio.create_task(asyncio.to_thread(self.scanner.run_scan, domain, request.scanType,request.checkLive ))
                return {
                    "status": "pending",
                    "progress": 0,
                    "step": "queued"
                }
            except HTTPException:
                raise
            except Exception as exc:
                logger.error("URL scan scheduling error", exc_info=True)
                raise HTTPException(status_code=500, detail="Error scheduling scan") from exc

    async def urlscan_ip(self, request: IPScanRequest):
        logger.info("Received request at /urlscan/ip")

        async with self.track_waiting("/urlscan/ip"):
            try:
                ip = request.ip.strip()
                if not ip:
                    raise HTTPException(status_code=400, detail="IP required")

                state = self.ip_scanner.get_ip_scan_status(ip)

                if state["status"] == "done":
                    return {"result": state["result"]}

                if state["status"] == "pending":
                    return {
                        "status": "pending",
                        "progress": state.get("progress", 0),
                        "step": state.get("step", "")
                    }

                asyncio.create_task(
                    asyncio.to_thread(self.ip_scanner.run_ip_scan, ip)
                )

                return {
                    "status": "pending",
                    "progress": 0,
                    "step": "queued"
                }

            except HTTPException:
                raise
            except Exception as exc:
                logger.error("IP scan scheduling error", exc_info=True)
                raise HTTPException(
                    status_code=500,
                    detail="Error scheduling IP scan"
                ) from exc

    async def nlp_embed(self, request: parse_semantic):
        logger.info("Received request at /nlp/embed")
        return await self.process_request(
            request=request.data,
            command=NLP_REQUEST_COMMANDS.S_EMBED,
            controller=self.nlp_controller_instance.invoke_trigger,
            default_result={},
            timeout=120,
            endpoint="/nlp/embed"
        )

    async def nlp_embed_index(self, request: embed_index_model):
        logger.info("Received request at /nlp/embed/index")
        return await self.process_request(
            request=request.data,
            command=NLP_REQUEST_COMMANDS.S_EMBED_INDEX,
            controller=self.nlp_controller_instance.invoke_trigger,
            default_result={},
            timeout=120,
            endpoint="/nlp/embed/index"
        )

    async def nlp_init(self, request: Request):
        logger.info("Received request at /nlp/init")
        payload = await request.json()
        return await self.process_request(
            request=payload,
            command=NLP_REQUEST_COMMANDS.S_INIT,
            controller=self.nlp_controller_instance.invoke_trigger,
            default_result={},
            timeout=120,
            endpoint="/nlp/init"
        )

    async def social_scrape(self, request: SocialScrapeRequest):
        logger.info("Received request at /social/scrape")
        async with self.track_waiting("/social/scrape"):
            try:
                targets = []

                if request.usernames and request.platform:
                    targets.append({
                        "platform": request.platform,
                        "usernames": request.usernames,
                        "max_followers": request.max_followers,
                        "max_following": request.max_following
                    })

                if request.targets:
                    for t in request.targets:
                        targets.append({
                            "platform": t.platform,
                            "usernames": t.usernames,
                            "max_followers": t.max_followers,
                            "max_following": t.max_following
                        })

                if not targets:
                    raise HTTPException(
                        status_code=400,
                        detail="Provide 'usernames' and 'platform', or 'targets' for multiple platforms"
                    )

                scrape_key = str(hash(str(targets)))
                state = self.social_controller_instance.get_scrape_status(scrape_key)

                if state["status"] == "done":
                    return {"scrape_key": scrape_key, "result": state["result"]}

                if state["status"] == "pending":
                    return {
                        "scrape_key": scrape_key,
                        "status": "pending",
                        "progress": state.get("progress", 0),
                        "step": state.get("step", "")
                    }

                data = {
                    "scrape_key": scrape_key,
                    "targets": targets,
                    "compare_results": request.compare_results if hasattr(request, 'compare_results') else True,
                    "similarity_threshold": request.similarity_threshold if hasattr(request,
                                                                                    'similarity_threshold') else 70
                }

                async def _run_with_timeout():
                    try:
                        await asyncio.wait_for(
                            asyncio.to_thread(
                                self.social_controller_instance.invoke_trigger,
                                SOCIAL_REQUEST_COMMANDS.S_SCRAPE_MULTIPLE,
                                data
                            ),
                            timeout=600
                        )
                    except asyncio.TimeoutError:
                        self.social_controller_instance.clear_scrape_status(scrape_key)

                asyncio.create_task(_run_with_timeout())

                return {
                    "scrape_key": scrape_key,
                    "status": "pending",
                    "progress": 0,
                    "step": "queued"
                }

            except HTTPException:
                raise
            except Exception as exc:
                logger.error("Social scrape scheduling error", exc_info=True)
                raise HTTPException(status_code=500, detail="Error scheduling scrape") from exc

    async def social_scrape_status(self, request: Request):
        logger.info("Received request at /social/scrape/status")
        try:
            payload = await request.json()
            scrape_key = payload.get("scrape_key")

            if not scrape_key:
                raise HTTPException(status_code=400, detail="scrape_key is required")

            state = self.social_controller_instance.get_scrape_status(scrape_key)

            if state["status"] == "new":
                return JSONResponse(
                    status_code=404,
                    content={"error": "Scrape job not found"}
                )

            return state

        except HTTPException:
            raise
        except Exception as exc:
            logger.error("Error checking scrape status", exc_info=True)
            raise HTTPException(status_code=500, detail="Error checking status") from exc

    async def ioc_extract(
            self,
            file: Optional[UploadFile] = File(None),
            text: Optional[str] = Form(None)
    ):

        logger.info("Received request at /ioc/extract")


        if text and not file:
            logger.info("Processing direct text input")
            return await self.process_request(
                request={'text': text},
                command=IOC_REQUEST_COMMANDS.S_EXTRACT,
                controller=self.ioc_controller_instance.invoke_trigger,
                default_result={},
                timeout=60,
                endpoint="/ioc/extract [text]"
            )


        if file:
            logger.info(f"Processing uploaded file: {file.filename}")


            content = await file.read()
            if len(content) > 50 * 1024 * 1024:
                raise HTTPException(status_code=413, detail="File too large (max 50MB)")

            async with self.track_waiting("/ioc/extract [file]"):
                temp_file_path = None
                try:

                    suffix = Path(file.filename).suffix
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                        temp_file.write(content)
                        temp_file_path = temp_file.name

                    logger.info(f"Processing file: {file.filename} (type: {suffix}) at temp path: {temp_file_path}")


                    result = await asyncio.wait_for(
                        self.ioc_controller_instance.invoke_trigger(
                            IOC_REQUEST_COMMANDS.S_EXTRACT,
                            {'file_path': temp_file_path}
                        ),
                        timeout=120
                    )


                    if result and isinstance(result, dict):
                        result['original_filename'] = file.filename

                    logger.info(f"Successfully processed {file.filename}")
                    return {"result": result}

                except asyncio.TimeoutError as exc:
                    logger.warning(f"IOC extraction timeout for {file.filename}")
                    raise HTTPException(status_code=504, detail="Processing timeout") from exc

                except ValueError as exc:

                    logger.error(f"Unsupported file type: {file.filename}")
                    raise HTTPException(status_code=400, detail=f"Unsupported file type: {str(exc)}") from exc

                except Exception as exc:
                    logger.error(f"IOC extraction error for {file.filename}", exc_info=True)
                    raise HTTPException(status_code=500, detail=f"Error processing file: {str(exc)}") from exc

                finally:

                    if temp_file_path and os.path.exists(temp_file_path):
                        try:
                            os.unlink(temp_file_path)
                            logger.info(f"Cleaned up temp file: {temp_file_path}")
                        except Exception as e:
                            logger.error(f"Failed to delete temp file {temp_file_path}: {e}")


        raise HTTPException(
            status_code=400,
            detail="Please provide either a 'file' (PDF/Image/Text) or 'text' parameter"
        )


api_service = APIService()
app = api_service.app
