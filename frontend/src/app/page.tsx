"use client";

import { getResumeMatch, uploadResume } from "@/utils/api";
import { Box, Button, Divider, Typography } from "@mui/material";
import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState<string>("");
  const [jobDescription, setJobDescription] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<{
    final_score: number;
    similarity: number;
    skill_match_score: number;
    common_skills: string[];
  } | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files ? e.target.files[0] : null;
    setFile(selectedFile);
    if (selectedFile) {
      setFileName(selectedFile.name);
    } else {
      setFileName("");
    }
  };

  const handleDescriptionChange = (
    e: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setJobDescription(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setAnalysis(null);

    if (!file) {
      setError("Please select a file to upload.");
      setLoading(false);
      return;
    }

    try {
      const uploadResponse = await uploadResume(file);
      setMessage("Resume uploaded successfully!");

      const analysisResponse = await getResumeMatch(
        uploadResponse,
        jobDescription
      );
      setAnalysis(analysisResponse);
    } catch (err) {
      setError("An error occurred during the process.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      bgcolor={"#1E293B"}
      borderRadius={"20px"}
      style={{ padding: "40px", maxWidth: "1000px", margin: "25px auto" }}
      display={"flex"}
      flexDirection={"column"}
      gap={2}
    >
      <Typography
        variant="h2"
        fontWeight={"bold"}
        align={"center"}
        color="#94A3B8"
        marginBottom={2}
      >
        Resume Analyzer
      </Typography>
      <form onSubmit={handleSubmit}>
        <Box
          display={"flex"}
          flexDirection={"row"}
          justifyContent={"space-between"}
          gap={2}
        >
          <div
            style={{
              width: "50%",
              display: "flex",
              flexDirection: "column",
              gap: 2,
            }}
          >
            <label htmlFor="file">
              <Typography
                variant="h6"
                fontWeight={"bold"}
                align={"center"}
                mb={2}
              >
                Upload Resume
              </Typography>
            </label>
            <div className="flex flex-col items-center gap-4">
              <label htmlFor="file">
                <Button variant="contained" component="span">
                  Choose File
                </Button>
              </label>
              <input
                type="file"
                id="file"
                name="file"
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
                className="hidden"
              />
              {fileName && (
                <Typography
                  variant="body1"
                  fontWeight={"bold"}
                  align={"center"}
                >
                  {fileName}
                </Typography>
              )}
            </div>
          </div>

          <div
            style={{
              width: "50%",
              display: "flex",
              flexDirection: "column",
              gap: 2,
            }}
          >
            <label htmlFor="jobDescription">
              <Typography
                variant="h6"
                fontWeight={"bold"}
                align={"center"}
                mb={2}
              >
                Job Description
              </Typography>
            </label>
            <textarea
              id="jobDescription"
              name="jobDescription"
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={handleDescriptionChange}
              required
              rows={5}
              className="border border-gray-300 rounded-md p-2 w-full text-black"
            />
          </div>
        </Box>
        <div
          style={{ display: "flex", justifyContent: "center", marginBlock: 40 }}
        >
          <Button
            variant="contained"
            type="submit"
            disabled={!file || !jobDescription}
            loading={loading}
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </Button>
        </div>

        {message && (
          <Typography color={"#94A3B8"} align={"center"}>
            {message}
          </Typography>
        )}
        {error && <p style={{ color: "red" }}>{error}</p>}
        {analysis !== null && (
          <div>
            <Typography variant="h6" fontWeight={"bold"} align={"center"}>
              Analysis Result:{" "}
              <span
                style={{
                  color: `hsl(${Math.min(
                    120,
                    Math.max(0, analysis.final_score * 1.2)
                  )}, 100%, 50%)`,
                }}
              >
                {analysis.final_score}
              </span>
            </Typography>
            <Typography variant="body1" align={"center"}>
              Similarity: {analysis.similarity}
            </Typography>
            <Typography variant="body1" align={"center"}>
              Skill Match: {analysis.skill_match_score}
            </Typography>
            <Typography variant="body1" align={"center"} mb={2}>
              Common Skills:{" "}
              {analysis.common_skills
                .map((skill) => skill.charAt(0).toUpperCase() + skill.slice(1))
                .join(", ")}
            </Typography>
          </div>
        )}
      </form>

      <Divider color="#ffffff" style={{ margin: "20px 0" }} />

      {file && file.type === "application/pdf" && (
        <Box>
          <Typography variant="h6" fontWeight="bold" align="center" mb={4}>
            Uploaded Resume Preview
          </Typography>
          <iframe
            src={URL.createObjectURL(file)}
            width="100%"
            height="600px"
            style={{ border: "none" }}
          />
        </Box>
      )}
    </Box>
  );
}
