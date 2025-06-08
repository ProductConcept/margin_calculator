import ast
from pathlib import Path
from types import SimpleNamespace


def load_entered():
    src = Path('app.py').read_text(encoding='utf-8')
    tree = ast.parse(src)
    func = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == '_entered')
    st = SimpleNamespace(session_state={})
    ns = {'st': st}
    module = ast.Module(body=[func], type_ignores=[])
    exec(compile(module, 'app.py', 'exec'), ns)
    return ns['_entered'], st.session_state


def test_entered_missing_key():
    _entered, state = load_entered()
    assert not _entered('missing')


def test_entered_stripped_blank():
    _entered, state = load_entered()
    state['val'] = '   '
    assert not _entered('val')


def test_entered_zero_value():
    _entered, state = load_entered()
    state['count'] = 0
    assert _entered('count')

