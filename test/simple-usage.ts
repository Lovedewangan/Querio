import { generateQuery } from "../src/queryGenerator";
import { QueryRequest } from "../src/types";
import dotenv from "dotenv";
dotenv.config();

async function runDemo() {
  const input: QueryRequest = {
    schema: {
      tables: [
        {
          name: "users",
          columns: [
            { name: "id", type: "int" },
            { name: "name", type: "varchar(255)" },
            { name: "email", type: "varchar(255)" }
          ]
        }
      ]
    },
    question: "Show all users with email ending in '@gmail.com'",
    model: "distilgpt2", // Using Mistral instead
    temperature: 0.1
  };

  try {
    const result = await generateQuery(input);
    console.log("Generated MySQL Query:\n", result.query);
    console.log("\nModel used:", result.modelUsed);
    
    // Validate the output looks like SQL
    if (!result.query.match(/SELECT.*FROM/i)) {
      console.warn("Warning: The output doesn't look like valid SQL");
    }
  } catch (error) {
    console.error("Error:", error instanceof Error ? error.message : String(error));
    console.log("\nTroubleshooting tips:");
    console.log("1. Verify your HUGGINGFACE_API_KEY in .env");
    console.log("2. Check your internet connection");
    console.log("3. Try a simpler query first");
  }
}

runDemo();