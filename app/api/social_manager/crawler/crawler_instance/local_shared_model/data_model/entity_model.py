from pydantic import BaseModel
from typing import List, Optional


class entity_model(BaseModel):
    m_email: Optional[List[str]] = None
    m_phone_numbers: Optional[List[str]] = None
    m_states: Optional[List[str]] = None
    m_location: Optional[List[str]] = None
    m_social_media_profiles: Optional[List[str]] = None
    m_social_channel: Optional[List[str]] = None
    m_confidence: Optional[List[str]] = None
    m_name: Optional[str] = None
    m_id_card_number: Optional[List[str]] = None
    m_username: Optional[List[str]] = None
    m_employee_count: Optional[str] = None
    m_industry: Optional[str] = None
    m_company_name: Optional[str] = None
    m_country: Optional[List[str]] = None
    m_ip: Optional[List[str]] = None
    m_weblink: Optional[List[str]] = None
    m_team: Optional[str] = None
    m_attacker: Optional[List[str]] = None
    m_code_snippet: Optional[List[str]] = None
    m_risk: Optional[List[str]] = None
    m_remote_type: Optional[List[str]] = None
    m_cve: Optional[List[str]] = None
    m_cwe: Optional[List[str]] = None
    m_cve_source: Optional[List[str]] = []
    m_severity: Optional[str] = None
    m_architecture: Optional[List[str]] = None
    m_author: Optional[List[str]] = None
    m_platform: Optional[List[str]] = None
    m_cvss: Optional[List[str]] = None
    m_solution: Optional[str] = None
    m_hashtags: Optional[List[str]] = None
    m_external_scanners: Optional[List[str]] = None
    m_exploit_year: Optional[str] = None
    m_product: Optional[List[str]] = None
    m_version: Optional[str] = None
    m_vulnerability: Optional[str] = None
    m_github_links: Optional[List[str]] = None
    m_tags: Optional[List[str]] = None
    m_scrap_file: str = None
    m_total_report: Optional[str] = None
    m_isp: Optional[List[str]] = None
    m_leak_type: Optional[str] = None
    m_region: Optional[List[str]] = None
    m_district: Optional[List[str]] = None
    m_police_station: Optional[List[str]] = None
    m_complaint_record: Optional[List[str]] = None
    m_officer_name: Optional[List[str]] = None
    m_complaint_status: Optional[List[str]] = None
    m_offense: Optional[List[str]] = None
    m_Family_head_name: Optional[List[str]] = None
    m_dob: Optional[List[str]] = None
    m_family_no: Optional[List[str]] = None
    m_family_member_name: Optional[List[str]] = None

    model_config = {
        "extra": "allow"
    }
