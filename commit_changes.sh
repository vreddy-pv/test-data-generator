#!/bin/bash
git add .
git commit -m "feat: Enhance test data generator

- Add support for multiple database dialects (H2, MySQL, PostgreSQL).
- Implement topological sort for robust foreign key handling.
- Improve SQL parsing to extract detailed foreign key constraints.
- Update documentation and add sample schemas for new dialects."
