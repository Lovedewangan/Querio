import { Schema } from "./types";

export function buildPrompt(schema: Schema, question: string): string {
  const schemaDescription = schema.tables
    .map(table => {
      const columns = table.columns
        .map(col => `    • ${col.name} (${col.type})`)
        .join('\n');
      return `  • Table: ${table.name}\n${columns}`;
    })
    .join('\n\n');

  return `### Task
Generate a MySQL query to answer the question below using the provided database schema.

### Database Schema
${schemaDescription}

### Question
${question}

### Instructions
- Only output the SQL query
- Use proper MySQL syntax
- Do not include any explanations
- Ensure the query ends with a semicolon

### SQL Query
`;
}