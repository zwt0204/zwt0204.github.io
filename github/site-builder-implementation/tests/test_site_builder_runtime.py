from app.services import SiteBuilderRuntime


def test_happy_path_ds_build_ready():
    runtime = SiteBuilderRuntime()
    session_id = "t1"

    r1 = runtime.handle_message(session_id, "我要做一个珠宝站")
    assert r1["stage"] in {"collect_style", "base_confirm", "collect_industry"}

    r2 = runtime.handle_message(session_id, "英文，高级极简")
    assert r2["stage"] == "base_confirm"
    assert "luxury minimal" in r2["reply"]

    r3 = runtime.handle_message(session_id, "确认")
    assert r3["stage"] == "collect_product_mode"

    r4 = runtime.handle_message(session_id, "ds，home decor，美区，20-80 USD，30款")
    assert r4["stage"] == "product_confirm"

    r5 = runtime.handle_message(session_id, "确认")
    assert r5["stage"] == "build_ready"
    assert r5["build_job"]["job_type"] == "generate_ecommerce_site"
    assert "preview.example.com" in r5["reply"]


def test_none_showcase_path():
    runtime = SiteBuilderRuntime()
    session_id = "t2"

    runtime.handle_message(session_id, "我要做一个珠宝站")
    runtime.handle_message(session_id, "英文，高级极简")
    runtime.handle_message(session_id, "确认")
    r4 = runtime.handle_message(session_id, "先不做商品，做展示站")
    assert r4["stage"] == "product_confirm"

    r5 = runtime.handle_message(session_id, "确认")
    assert r5["build_job"]["job_type"] == "generate_showcase_site"


def test_modification_guard():
    runtime = SiteBuilderRuntime()
    session_id = "t3"

    runtime.handle_message(session_id, "我要做一个珠宝站")
    r2 = runtime.handle_message(session_id, "英文，高级极简")
    assert r2["stage"] == "base_confirm"

    r3 = runtime.handle_message(session_id, "可以，不过改成中文")
    assert r3["stage"] != "collect_product_mode"
    assert r3["state"]["base_confirmed"] is False


def test_reset_clears_state():
    runtime = SiteBuilderRuntime()
    session_id = "t4"

    runtime.handle_message(session_id, "我要做一个珠宝站")
    runtime.handle_message(session_id, "英文，高级极简")
    reset_result = runtime.reset(session_id)
    assert reset_result["state"]["industry"] is None
    assert reset_result["state"]["style"] is None
    assert reset_result["state"]["product_source_mode"] is None


def test_product_confirm_supports_modification_and_reconfirm():
    runtime = SiteBuilderRuntime()
    session_id = "t5"

    runtime.handle_message(session_id, "我要做一个珠宝站")
    runtime.handle_message(session_id, "英文，高级极简")
    runtime.handle_message(session_id, "确认")
    runtime.handle_message(session_id, "ds，home decor，美区，20-80 USD，30款")

    r = runtime.handle_message(session_id, "可以，不过改成 jewelry，美区，30-100 USD，50款")
    assert r["stage"] == "product_confirm"
    assert r["state"]["product_ds_criteria"]["category"] == "jewelry"
    assert r["state"]["product_ds_criteria"]["market"] == "US"
    assert r["state"]["product_ds_criteria"]["price_range"] == "30-100 usd"
    assert r["state"]["product_ds_criteria"]["quantity_target"] == "50"
    assert r["state"]["product_phase_confirmed"] is False


def test_base_confirm_supports_modification_and_reconfirm():
    runtime = SiteBuilderRuntime()
    session_id = "t6"

    runtime.handle_message(session_id, "我要做一个珠宝站")
    runtime.handle_message(session_id, "英文，高级极简")
    r = runtime.handle_message(session_id, "可以，不过改成中文")
    assert r["stage"] == "base_confirm"
    assert r["state"]["language"] == "zh"
    assert r["state"]["base_confirmed"] is False
    assert "语言=zh" in r["reply"]


def test_product_phase_industry_change_falls_back_to_base_confirm():
    runtime = SiteBuilderRuntime()
    session_id = "t7"

    runtime.handle_message(session_id, "我要做一个珠宝站")
    runtime.handle_message(session_id, "英文，高级极简")
    runtime.handle_message(session_id, "确认")
    runtime.handle_message(session_id, "ds，home decor，美区，20-80 USD，30款")

    r = runtime.handle_message(session_id, "可以，不过行业改成 beauty")
    assert r["stage"] == "collect_style"
    assert r["state"]["industry"] == "beauty"
    assert r["state"]["style"] is None
    assert r["state"]["base_confirmed"] is False
    assert r["state"]["product_phase_confirmed"] is False
    assert "风格还没定" in r["reply"]
    assert "elegant clean" in r["reply"]


def test_current_stage_is_persisted_in_state():
    runtime = SiteBuilderRuntime()
    session_id = "t8"

    r1 = runtime.handle_message(session_id, "我要做一个珠宝站")
    assert r1["state"]["current_stage"] == r1["stage"]

    r2 = runtime.handle_message(session_id, "英文，高级极简")
    assert r2["state"]["current_stage"] == r2["stage"]
