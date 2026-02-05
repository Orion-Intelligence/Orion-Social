from typing import Dict, Any
from .ioc_extractor import IOCExtractor
from .ioc_enums import IOC_REQUEST_COMMANDS, IOC_EXTRACTION_STATUS
from api.nlp_manager. pii_manager. pii_controller import pii_controller


class ioc_controller:


    def __init__(self):
        self.extractor = IOCExtractor()
        self.pii_parser = pii_controller()

    async def invoke_trigger(self, command: int, data: Any = None) -> Any:


        if command == IOC_REQUEST_COMMANDS.S_EXTRACT:
            return await self._extract_iocs(data)

        return None

    async def _extract_iocs(self, data: Dict[str, Any]) -> Dict[str, Any]:


        if isinstance(data, dict) and 'text' in data:
            return await self._parse_text_directly(data['text'])


        file_path = data. get('file_path') if isinstance(data, dict) else data


        extraction_result = self.extractor.extract_text(file_path)

        if extraction_result['status'] != IOC_EXTRACTION_STATUS. SUCCESS:
            return {
                    **extraction_result,
                "iocs": []
            }


        extracted_text = extraction_result['extracted_text']
        iocs = await self.pii_parser. parse(extracted_text[0:3000])


        return {
            "filename": extraction_result['filename'],
            "file_type": extraction_result['file_type'],
            "extracted_text_length": extraction_result['extracted_text_length'],
            "iocs": iocs,
            "status": IOC_EXTRACTION_STATUS.SUCCESS
        }

    async def _parse_text_directly(self, text: str) -> Dict[str, Any]:

        if not text or not text.strip():
            return {
                "extracted_text_length": 0,
                "iocs": [],
                "status": IOC_EXTRACTION_STATUS.ERROR,
                "error_message": "No text provided"
            }


        iocs = await self.pii_parser.parse(text[0:3000])

        return {
            "extracted_text_length": len(text),
            "iocs": iocs,
            "status": IOC_EXTRACTION_STATUS.SUCCESS
        }