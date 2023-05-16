"""The tests in this module are run against a real bamboo instance."""

from bamboohbn.main import (get_builds_running_longer_than, get_running_builds,
                            notify_ms_teams_about_hanging_builds,
                            send_ms_teams_notification, show_build)

TEST_PLAN_KEY = "TEST-PLAN"
WEB_HOOK_URL = "https://ms_teams_webhook_url"

def test_get_running_builds():
    """Test get running builds"""
    test_plan_key = TEST_PLAN_KEY
    builds = get_running_builds(test_plan_key)
    assert len(builds) >= 0

def test_show_build():
    """Test show builds"""
    test_plan_key = TEST_PLAN_KEY
    test_build_number = "2"
    build_details = show_build(test_plan_key, test_build_number)
    assert "progress" in build_details

    test_plan_key = TEST_PLAN_KEY
    test_build_number = "222"
    build_details = show_build(test_plan_key, test_build_number)
    assert build_details == {}

def test_get_builds_running_longer_than():
    """Test get builds running longer than"""
    test_plan_key = TEST_PLAN_KEY
    time_threshold_seconds = 3600

    hanging_builds = get_builds_running_longer_than(test_plan_key, time_threshold_seconds)
    assert len(hanging_builds) >= 0

def test_notify_ms_teams_about_hanging_builds():
    """Test notification to ms teams about hanging builds"""
    test_plan_key = TEST_PLAN_KEY
    #This will send a message to MS Teams channel
    notify_ms_teams_about_hanging_builds(test_plan_key)

def test_send_ms_teams_notification():
    """Test notification to ms teams"""
    message = "testing ms teams web hook from python code"
    #This will send a message to MS Teams channel
    send_ms_teams_notification(WEB_HOOK_URL, message)
