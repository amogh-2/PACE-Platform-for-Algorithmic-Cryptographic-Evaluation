document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded and parsed");

  const runButton = document.querySelector(".run-button");
  const resultsTable = document.querySelector("table tbody");
  const fileSize = document.getElementById("fileSize");

  // Check if elements are found
  console.log("runButton:", runButton);
  console.log("resultsTable:", resultsTable);
  console.log("fileSize:", fileSize);

  // Load existing benchmark results when the page loads
  loadExistingResults();

  if (runButton) {
      runButton.addEventListener("click", async () => {
          console.log("Run Benchmark clicked");
          // Disable button during benchmark
          runButton.disabled = true;
          runButton.textContent = "Running Benchmark...";

          try {
              // Get selected file size
              const selectedSize = fileSize.value;

              // Call the benchmark endpoint
              const response = await fetch("/run_benchmark", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                  },
                  body: JSON.stringify({ fileSize: selectedSize, algorithm: "AES-CBC" }),
              });

              if (!response.ok) {
                  throw new Error("Benchmark failed");
              }

              const result = await response.json();

              // Add the new result to the table
              addResultRow(result);

              // Re-enable the button
              runButton.textContent = "Run Benchmark";
              runButton.disabled = false;
          } catch (error) {
              console.error("Error running benchmark:", error);
              runButton.textContent = "Run Benchmark";
              runButton.disabled = false;
              alert("Error running benchmark. Please try again.");
          }
      });
  }

  async function loadExistingResults() {
      try {
          // Get selected file size
          const selectedSize = fileSize.value;

          // Call the API to get existing results
          const response = await fetch(`/get_benchmark_results?algorithm=AES-CBC&fileSize=${selectedSize}`);

          if (!response.ok) {
              throw new Error("Failed to load benchmark results");
          }

          const results = await response.json();

          // Clear existing table rows
          resultsTable.innerHTML = "";

          // Add each result to the table
          results.forEach((result) => {
              addResultRow(result);
          });
      } catch (error) {
          console.error("Error loading benchmark results:", error);
      }
  }

  // Listen for changes to the file size dropdown
  if (fileSize) {
      fileSize.addEventListener("change", () => {
          console.log("File size changed to:", fileSize.value);
          loadExistingResults();
      });
  }

  function addResultRow(result) {
      const newRow = resultsTable.insertRow();

      // Add cells with result data
      const cpuCell = newRow.insertCell();
      cpuCell.textContent = result.cpu_model;

      const osCell = newRow.insertCell();
      osCell.textContent = result.os_name;

      const fileSizeCell = newRow.insertCell();
      fileSizeCell.textContent = result.file_size;

      const encTimeCell = newRow.insertCell();
      encTimeCell.textContent = result.encryption_time + "s";

      const decTimeCell = newRow.insertCell();
      decTimeCell.textContent = result.decryption_time + "s";

      const execTimeCell = newRow.insertCell();
      execTimeCell.textContent = result.execution_time + "s";
  }
});