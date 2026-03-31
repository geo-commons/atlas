# Contributing

Welcome to Atlas! This document outlines the guidelines and conventions for contributing to our codebase. Following these standards helps us maintain a consistent, maintainable, and high-quality application.

Please read this guide carefully before submitting changes. It covers expectations around code style, architecture, testing, and collaboration. In general:

- Code is written in English
- Communication (PRs, issues, discussions) is in Dutch
- We favor clarity, consistency, and minimal complexity

By contributing, you agree to follow these guidelines to ensure smooth collaboration between developers, reviewers, and stakeholders.

## Structure

### General

- Minimize adding new dependencies
- Use descriptive naming for functions, variables, and classes
- Code must be written in English
- PR descriptions, issues, and discussions must be written in Dutch (for stakeholder visibility)

### Frontend Guidelines

**Framework & Architecture**

- Use Vue Composition API for all new components
- Refactor small legacy components to Composition API when touched
- Use TypeScript in:
  - All new components
  - Refactored legacy components

**State Management**

- Do not use storeToRefs if its not necessary to use, see: (https://masteringpinia.com/blog/my-top-5-tips-for-using-pinia)
- Use Pinia stores directly as reactive Vue hooks

**Code Quality**

- Prefer enums where applicable
- Avoid unnecessary any types
- Use strict TypeScript definitions

**Testing**

- All new utility functions must have unit tests

**Style**

- Use arrow functions instead of classic function declarations

### Backend Guidelines

- Prefer built-in functionality of existing libraries (especially Django)
- All backend changes must include tests
- Add type annotations where possible

### Testing Strategy

- Test contracts between app and external libraries (integration tests if needed)
- Critical parts must always be covered:
  - Authentication
  - Authorization
