# Artifact Anatomy Answer Key

## plan.json
- **Writer**: subplanner (jg-subplanner)
- **Required fields**: affected_files, steps, acceptance_mapping
- **Consumer**: worker (jg-worker) -- reads steps and affected_files to know what to implement

## worker-result.json
- **Writer**: worker (jg-worker)
- **Required fields**: status, files_changed, blockers, summary
- **Consumer**: tester (jg-tester) -- reads to know what files changed, then runs tests

## debug-diagnosis.json
- **Writer**: debugger (jg-debugger)
- **Required fields**: failure_source, failure_description, root_cause, root_cause_file, root_cause_line, classification
- **Consumer**: worker (jg-worker) -- reads root_cause and fix_instructions to apply the fix
