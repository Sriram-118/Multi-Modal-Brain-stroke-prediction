from pathlib import Path

content = Path('StrokeApp/templates/Predict.html').read_text(encoding='utf-8')
print('CSRF token found:', 'csrf_token' in content)
print('t1 found:', 'name="t1"' in content)
print('t2 found:', 'name="t2"' in content)
print('t3 found:', 'name="t3"' in content)
print('t4 found:', 'name="t4"' in content)
print('t5 found:', 'name="t5"' in content)
print('t6 found:', 'name="t6"' in content)
print('t7 found:', 'name="t7"' in content)
print('Bootstrap classes found:', 'form-control' in content or 'form-select' in content)
