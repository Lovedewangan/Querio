import { Schema, Table } from "./types";

export function parseSchema(rawSchema: any): Schema {
  if (!rawSchema.tables || !Array.isArray(rawSchema.tables)) {
    throw new Error("Invalid schema format");
  }

  return {
    tables: rawSchema.tables.map((table: any): Table => ({
      name: table.name,
      columns: table.columns.map((col: any) => ({
        name: col.name,
        type: col.type
      }))
    }))
  };
}