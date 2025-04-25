export interface Column {
    name: string;
    type: string;
  }
  
  export interface Table {
    name: string;
    columns: Column[];
  }
  
  export interface Schema {
    tables: Table[];
  }
  
  export interface QueryRequest {
    schema: Schema;
    question: string;
    // Add the optional properties that were referenced in queryGenerator.ts
    model?: string;
    temperature?: number;
  }
  
  export interface QueryResponse {
    query: string;
    // Add the properties referenced in queryGenerator.ts
    prompt: string;
    modelUsed: string;
    confidence?: number;
  }