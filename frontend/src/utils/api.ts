import axios from "axios";

const API_URL = "http://localhost:8080";

const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

export const uploadResume = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await axiosInstance.post("/upload/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data.text;
};

export const getResumeMatch = async (
  resumeText: string,
  jobDescription: string
) => {
  const formData = new FormData();
  formData.append("resume_text", resumeText);
  formData.append("job_description", jobDescription);
  const response = await axiosInstance.post("/match/", formData);
  console.log(response.data);
  return response.data.score;
};
