import { HfInference } from "@huggingface/inference";
import { buildPrompt } from "./promptBuilder";
import { parseSchema } from "./schemaParser";
import { QueryRequest, QueryResponse } from "./types";

export async function generateQuery(request: QueryRequest): Promise<QueryResponse> {
  if (!request.schema || !request.question) {
    throw new Error("Missing required fields: schema and question must be provided");
  }

  const schema = parseSchema(request.schema);
  const prompt = buildPrompt(schema, request.question);
  
  try {
    const hf = new HfInference(process.env.HUGGINGFACE_API_KEY);
    
    // Using Mistral-7B which is widely available
const model = request.model || "mistralai/Mistral-7B-Instruct-v0.2";

    
    const response = await hf.textGeneration({
      model: model,
      inputs: prompt,
      parameters: {
        max_new_tokens: 200,
        temperature: request.temperature || 0.1,
        top_p: 0.95,
        do_sample: true,
        return_full_text: false,
        stop_sequences: [";", "```"] // Stop at SQL delimiters
      }
    });
    
    let generatedQuery = response.generated_text.trim();
    
    // Enhanced cleaning for Mistral's output
    generatedQuery = generatedQuery
      .replace(/^```sql|```$/g, '')
      .replace(/^SELECT/i, 'SELECT')
      .split(';')[0]
      .trim();
    
    return {
      query: generatedQuery + (generatedQuery.endsWith(';') ? '' : ';'),
      prompt: prompt,
      modelUsed: model
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to generate SQL query: ${errorMessage}`);
  }
}