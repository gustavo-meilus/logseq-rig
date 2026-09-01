## RENAMED Requirements

- FROM: `### Requirement: Logical pages resolve through vault conventions`
- TO: `### Requirement: Logical pages resolve through graph conventions`

## MODIFIED Requirements

### Requirement: Logical pages resolve through graph conventions
Resolve SHALL map supported logical page names and reliably parsed aliases to canonical logical identity and actual source file using the detected graph descriptor and configured graph conventions.

#### Scenario: Logical name differs from filename
- **WHEN** a supported logical page name maps to an encoded or otherwise different filename
- **THEN** resolve returns the logical identity and actual source path
