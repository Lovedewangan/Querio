import axios from "axios";
import * as dotenv from "dotenv";

dotenv.config();

async function checkHuggingFaceToken() {
  const token = process.env.HUGGINGFACE_API_KEY;
  if (!token) {
    console.error("❌ HUGGINGFACE_API_KEY not found in environment.");
    return;
  }

  try {
    const response = await axios.get("https://huggingface.co/api/whoami-v2", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    console.log("✅ API token is valid.");
    console.log("User info:", response.data);
  } catch (error: any) {
    if (axios.isAxiosError(error)) {
      console.error("❌ Axios error:", error.response?.status, error.response?.data);
    } else {
      console.error("❌ Unexpected error:", error.message);
    }
  }
}

checkHuggingFaceToken();
