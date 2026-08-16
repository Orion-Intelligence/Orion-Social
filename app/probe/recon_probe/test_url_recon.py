from unittest.mock import patch

from api.social_manager.social_recon.extractors.username_extractor import username_extractor
from api.social_manager.social_recon.social_recon import social_recon


def test_url_targets_match_only_the_related_profile_site() -> None:
    assert username_extractor._url_targets("https://www.kickstarter.com/profile/msmannan00") == [
        ("Kickstarter", "msmannan00")
    ]


def test_url_targets_accept_scheme_less_and_common_profile_variants() -> None:
    assert ("Twitter", "elonmusk") in username_extractor._url_targets("x.com/elonmusk")
    assert ("YouTube", "Google") in username_extractor._url_targets("youtube.com/@Google")
    assert ("Kickstarter", "msmannan00") in username_extractor._url_targets(
        "kickstarter.com/profile/msmannan00?tab=repositories"
    )


def test_url_targets_reject_non_profile_routes() -> None:
    assert username_extractor._url_targets("https://www.reddit.com/r/python/comments/abc123") == []


def test_social_recon_routes_urls_to_url_only_extraction() -> None:
    expected = [{"metadata": {"platform": "Kickstarter", "username": "msmannan00"}}]
    with patch.object(username_extractor, "extract_url", return_value=expected) as extract_url:
        result = social_recon().parse("https://www.kickstarter.com/profile/msmannan00")

    assert result == expected
    extract_url.assert_called_once_with("https://www.kickstarter.com/profile/msmannan00", progress=None)


def test_url_extraction_scans_only_the_matched_site() -> None:
    with patch.object(username_extractor, "extract", return_value=[]) as extract:
        username_extractor.extract_url("https://www.kickstarter.com/profile/msmannan00")

    extract.assert_called_once_with("msmannan00", progress=None, site_names={"Kickstarter"})


def test_custom_recon_routes_known_platform_urls_to_entity_types() -> None:
    from api.social_manager.social_recon.custom_recon.custom_recon import custom_recon

    cases = {
        "https://x.com/elonmusk": ("X", "elonmusk", "profile"),
        "twitter.com/elonmusk/status/123": ("X", "elonmusk", "post"),
        "https://www.reddit.com/r/python/comments/abc123/title/": ("Reddit", "abc123", "post"),
        "reddit.com/r/python": ("Reddit", "python", "subreddit"),
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ": ("YouTube", "dQw4w9WgXcQ", "video"),
        "facebook.com/groups/12345/": ("Facebook", "12345", "group"),
    }
    for url, expected in cases.items():
        module, identity, target, _ = custom_recon._route(url)
        assert (module.constants.NAME, identity, target) == expected
    assert custom_recon._route("https://www.kickstarter.com/profile/msmannan00") is None


def test_social_recon_prefers_custom_recon_and_skips_maigret_for_known_platforms() -> None:
    from api.social_manager.social_recon.custom_recon.custom_recon import custom_recon

    expected = [{"metadata": {"platform": "X", "username": "elonmusk", "target_type": "profile"}}]
    with patch.object(custom_recon, "extract_url", return_value=expected), patch.object(
        username_extractor, "extract_url"
    ) as maigret:
        assert social_recon().parse("https://x.com/elonmusk") == expected
    maigret.assert_not_called()
