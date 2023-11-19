import pytest
import json


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    x = yield
    max_score = 1
    max_score = next(item.iter_markers('score')).args[0]
    x._result.max_score = max_score

def pytest_terminal_summary(terminalreporter, exitstatus):
    all_tests = []
    if ('passed' in terminalreporter.stats):
        all_tests = all_tests + terminalreporter.stats['passed']
    if ('failed' in terminalreporter.stats):
        all_tests = all_tests + terminalreporter.stats['failed']

    total_score = 0
    score = 0
    for s in all_tests:
        total_score += s.max_score
        if (s.outcome == 'passed'):
            score += s.max_score

    terminalreporter.ensure_newline()
    terminalreporter.write('\n\nLa nota orientativa obtenida en la práctica es:')
    terminalreporter.write('\n\n-----------------\n')
    terminalreporter.write('| Score: {} / {}|\n'.format(score, total_score))
    terminalreporter.write('-----------------\n')
