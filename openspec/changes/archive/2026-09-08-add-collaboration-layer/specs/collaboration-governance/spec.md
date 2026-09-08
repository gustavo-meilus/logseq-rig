## Purpose

Defines the public repository contract for safe, reviewable community contributions to Logseq Rig without expanding its runtime or graph ownership.

## ADDED Requirements

### Requirement: Repository presents a clear collaboration entrypoint
The repository SHALL publish an MIT license, a contributor guide, a code of conduct, a security policy, and README links that direct contributors to the appropriate collaboration channel. The contributor guide SHALL define the focused-change workflow, required development checks, OpenSpec expectations for behavior changes, and the project's graph-ownership boundaries.

#### Scenario: Contributor prepares a change
- **WHEN** a contributor opens the repository before making a change
- **THEN** they can identify the license, contribution workflow, required checks, design constraints, and routes for questions, issues, and security reports from version-controlled documentation

### Requirement: Security reports have a private reporting route
The security policy SHALL direct reporters to GitHub private vulnerability reporting when enabled and SHALL provide `gmeilus@outlook.com` as a private fallback. It MUST instruct reporters not to disclose exploitable vulnerabilities in public issues and SHALL state supported versions, report details to include, and the expected acknowledgement and handling process.

#### Scenario: Reporter identifies a vulnerability
- **WHEN** a reporter reads the security policy before opening an issue
- **THEN** they receive a private reporting route and the information needed to submit a useful report without public disclosure

### Requirement: GitHub intake captures actionable contribution information
The repository SHALL provide bug and feature issue forms and a pull-request template. The bug form SHALL collect environment, graph type, command, expected and actual results, reproduction steps, and sanitized output. The pull-request template SHALL collect the change rationale, verification evidence, documentation and OpenSpec status, and graph-safety impact.

#### Scenario: Contributor opens a bug or pull request
- **WHEN** a contributor selects a supported issue type or opens a pull request
- **THEN** GitHub presents the structured fields and checklists required to evaluate the report or change

### Requirement: Contributions receive automated and ownership checks
The repository SHALL define a GitHub Actions workflow that runs on pull requests to `main` and pushes to `main`, installs the package with Python 3.11, runs the unit suite and fast release validation, and checks whitespace errors. The repository SHALL assign `@gustavo-meilus` as owner of all paths and of `.github/` specifically.

#### Scenario: Pull request changes repository content
- **WHEN** a pull request targets `main`
- **THEN** the continuous-integration workflow runs the documented automated checks and GitHub identifies the responsible code owner

### Requirement: Repository declares its canonical local verification command
The repository SHALL declare its existing full release-validation command as the canonical local verification command. The command MUST retain the existing comprehensive release checks rather than introducing a duplicate check script.

#### Scenario: Contributor needs final verification
- **WHEN** a contributor or automation needs the repository's definitive local verification command
- **THEN** the project configuration identifies the existing full release-validation command unambiguously

### Requirement: Maintainer settings protect the default branch
Repository administrators SHALL enable Discussions and private vulnerability reporting, and SHALL protect `main` against force pushes and deletions while requiring pull requests, passing CI, and resolved review conversations before merge. Required approvals SHALL remain disabled until a second trusted maintainer can satisfy them without blocking routine maintenance.

#### Scenario: Maintainer configures repository governance
- **WHEN** the collaboration layer is deployed to GitHub
- **THEN** the documented repository settings provide the specified branch protections and communication channels
