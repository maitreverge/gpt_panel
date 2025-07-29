# Tests for Price_engine.py

def test_price_engine_init_and_total_spent(tmp_path, monkeypatch):
    # Prepare a fake CSV file for prices
    csv_content = "model,input,output,cache\nmodelA,100,200,300\n"
    price_file = tmp_path / "price_models.csv"
    price_file.write_text(csv_content)
    monkeypatch.setattr("Price_engine.PRICE_FILE", str(price_file))
    from Price_engine import Price_engine
    pe = Price_engine()
    assert isinstance(pe.prices, dict)
    assert "modelA" in pe.prices
    assert pe._total_spent == 0
    assert pe.total_spent.startswith("Total spent : $0.00000000")

def test_price_parser_structure(tmp_path, monkeypatch):
    csv_content = "model,input,output,cache\nm1,10,20,30\n"
    price_file = tmp_path / "price_models.csv"
    price_file.write_text(csv_content)
    monkeypatch.setattr("Price_engine.PRICE_FILE", str(price_file))
    from Price_engine import Price_engine
    pe = Price_engine()
    d = pe.price_parser()
    assert isinstance(d, dict)
    assert "m1" in d
    assert set(d["m1"].keys()) == {"input", "output", "cache"}

# Tests for Gpt_engine.py

def test_gpt_engine_init_reads_api_key(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("OPEN_AI_KEY=sk-testkey\n")
    monkeypatch.chdir(tmp_path)
    from Gpt_engine import Gpt_engine
    ge = Gpt_engine()
    assert ge._api_key == "sk-testkey\n"
    assert isinstance(ge.models, list)
    assert ge.lenght_choice == 3

def test_gpt_engine_init_lenght_choice(tmp_path, monkeypatch):
    prompt_dir = tmp_path / "assets" / "prompt_lenght"
    prompt_dir.mkdir(parents=True)
    prompt_file = prompt_dir / "prompt_length.md"
    prompt_file.write_text("1 - \nInstruction1\n2 - \nInstruction2\n3 - \nInstruction3\n4 - \nInstruction4\n5 - \nInstruction5\n")
    monkeypatch.chdir(tmp_path)
    from Gpt_engine import Gpt_engine
    ge = Gpt_engine()
    d = ge.init_lenght_choice()
    assert isinstance(d, dict)
    assert 1 in d and 5 in d

# Tests for Api_validator.py

def test_access_key_reads_env(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("OPEN_AI_KEY=sk-testkey\n")
    monkeypatch.chdir(tmp_path)
    from Api_validator import Api_validator
    av = Api_validator()
    key = av.access_key()
    assert key == "sk-testkey\n"

# Tests for Api_window.py

def test_api_window_init_properties():
    from Api_window import Api_window
    win = Api_window()
    assert hasattr(win, "api_key")
    assert hasattr(win, "env_path")
    assert win.api_key == ""
    assert isinstance(win.welcome_text, str)
    win.destroy()

def test_toplevel_window_label_text():
    from Api_window import ToplevelWindow
    win = ToplevelWindow(txt_input="Hello")
    assert "Hello" in win.label.cget("text")
    win.destroy()