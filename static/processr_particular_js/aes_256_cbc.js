document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded and parsed - AES-256-CBC");

  const runButton = document.querySelector(".run-button");
  const resultsTable = document.querySelector("table tbody");
  const fileSize = document.getElementById("fileSize");

  // Check if elements are found
  console.log("runButton:", runButton);
  console.log("resultsTable:", resultsTable);
  console.log("fileSize:", fileSize);

  if (!runButton) console.error("Run button not found!");
  if (!resultsTable) console.error("Results table not found!");
  if (!fileSize) console.error("File size selector not found!");

  // Load existing benchmark results when the page loads
  loadExistingResults();

  if (runButton) {
      runButton.addEventListener("click", async () => {
          console.log("Run Benchmark clicked - AES-256-CBC");
          runButton.disabled = true;
          runButton.textContent = "Running Benchmark...";

          try {
              const selectedSize = fileSize.value;
              console.log("Selected file size:", selectedSize);

              const response = await fetch("/run_benchmark", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                  },
                  body: JSON.stringify({ fileSize: selectedSize, algorithm: "AES-256-CBC" }),
              });

              console.log("Fetch response status:", response.status);
              if (!response.ok) {
                  const errorText = await response.text();
                  throw new Error(`Benchmark failed: ${errorText}`);
              }

              const result = await response.json();
              console.log("Benchmark result:", result);

              addResultRow(result);
              runButton.textContent = "Run Benchmark";
              runButton.disabled = false;
          } catch (error) {
              console.error("Error running benchmark:", error);
              runButton.textContent = "Run Benchmark";
              runButton.disabled = false;
              alert("Error running benchmark: " + error.message);
          }
      });
  }

  async function loadExistingResults() {
      try {
          const selectedSize = fileSize.value;
          const response = await fetch(`/get_benchmark_results?algorithm=AES-256-CBC&fileSize=${selectedSize}`);

          console.log("Get results response status:", response.status);
          if (!response.ok) {
              const errorText = await response.text();
              throw new Error(`Failed to load results: ${errorText}`);
          }

          const results = await response.json();
          console.log("Loaded results:", results);

          resultsTable.innerHTML = "";
          results.forEach((result) => addResultRow(result));
      } catch (error) {
          console.error("Error loading benchmark results:", error);
      }
  }

  if (fileSize) {
      fileSize.addEventListener("change", () => {
          console.log("File size changed to:", fileSize.value);
          loadExistingResults();
      });
  }

  function addResultRow(result) {
      const newRow = resultsTable.insertRow();
      newRow.insertCell().textContent = result.cpu_model;
      newRow.insertCell().textContent = result.os_name;
      newRow.insertCell().textContent = result.file_size;
      newRow.insertCell().textContent = result.encryption_time + "s";
      newRow.insertCell().textContent = result.decryption_time + "s";
      newRow.insertCell().textContent = result.execution_time + "s";
  }
});