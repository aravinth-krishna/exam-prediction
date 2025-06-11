// frontend/app/page.tsx
"use client";

import { useState, ChangeEvent, FormEvent } from "react";
import styles from "./HomePage.module.css";

interface PredictPayload {
  gender: string;
  race_ethnicity: string;
  parental_level_of_education: string;
  lunch: string;
  test_preparation_course: string;
  reading_score: number;
  writing_score: number;
}

export default function HomePage() {
  const [formData, setFormData] = useState<PredictPayload>({
    gender: "female",
    race_ethnicity: "group B",
    parental_level_of_education: "bachelor's degree",
    lunch: "standard",
    test_preparation_course: "completed",
    reading_score: 0,
    writing_score: 0,
  });
  const [result, setResult] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleChange(e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: e.target.type === "number" ? Number(value) : value,
    }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || res.statusText);
      }

      const data = (await res.json()) as { predicted_score: number };
      setResult(data.predicted_score);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to fetch prediction");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className={styles.container}>
      <h1 className={styles.title}>Exam Result Predictor</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label htmlFor="gender" className={styles.label}>
            Gender:
          </label>
          <select
            id="gender"
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            className={styles.select}
          >
            <option value="female">Female</option>
            <option value="male">Male</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="race_ethnicity" className={styles.label}>
            Race/Ethnicity:
          </label>
          <select
            id="race_ethnicity"
            name="race_ethnicity"
            value={formData.race_ethnicity}
            onChange={handleChange}
            className={styles.select}
          >
            <option value="group A">Group A</option>
            <option value="group B">Group B</option>
            <option value="group C">Group C</option>
            <option value="group D">Group D</option>
            <option value="group E">Group E</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="parental_level_of_education" className={styles.label}>
            Parental Education:
          </label>
          <select
            id="parental_level_of_education"
            name="parental_level_of_education"
            value={formData.parental_level_of_education}
            onChange={handleChange}
            className={styles.select}
          >
            <option value="some high school">Some High School</option>
            <option value="high school">High School</option>
            <option value="some college">Some College</option>
            <option value="associate's degree">Associate&apos;s Degree</option>
            <option value="bachelor's degree">Bachelor&apos;s Degree</option>
            <option value="master's degree">Master&apos;s Degree</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="lunch" className={styles.label}>
            Lunch:
          </label>
          <select
            id="lunch"
            name="lunch"
            value={formData.lunch}
            onChange={handleChange}
            className={styles.select}
          >
            <option value="standard">Standard</option>
            <option value="free/reduced">Free/Reduced</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="test_preparation_course" className={styles.label}>
            Test Preparation:
          </label>
          <select
            id="test_preparation_course"
            name="test_preparation_course"
            value={formData.test_preparation_course}
            onChange={handleChange}
            className={styles.select}
          >
            <option value="none">None</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="reading_score" className={styles.label}>
            Reading Score:
          </label>
          <input
            type="number"
            id="reading_score"
            name="reading_score"
            value={formData.reading_score}
            onChange={handleChange}
            min={0}
            max={100}
            className={styles.input}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="writing_score" className={styles.label}>
            Writing Score:
          </label>
          <input
            type="number"
            id="writing_score"
            name="writing_score"
            value={formData.writing_score}
            onChange={handleChange}
            min={0}
            max={100}
            className={styles.input}
            required
          />
        </div>

        <button type="submit" disabled={loading} className={styles.button}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </form>

      {error && <p className={styles.error}>Error: {error}</p>}
      {result !== null && !error && (
        <p className={styles.result}>
          Predicted Math Score: {result.toFixed(2)}
        </p>
      )}
    </main>
  );
}
