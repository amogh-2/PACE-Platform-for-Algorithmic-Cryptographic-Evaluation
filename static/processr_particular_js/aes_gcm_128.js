// aes_gcm_128.js
document.addEventListener("DOMContentLoaded", () => {
    const runButton = document.querySelector(".run-button")
    const resultsTable = document.querySelector("table")
    const fileSize = document.getElementById("file-size")
  
    runButton.addEventListener("click", async () => {
      // Disable button during benchmark
      runButton.disabled = true
      runButton.textContent = "Running Benchmark..."
  
      try {
        // Get selected file size
        const selectedSize = fileSize.value
  
        // Call the benchmark endpoint
        const response = await fetch("/run_benchmark", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ fileSize: selectedSize, algorithm: "AES-GCM" }),
        })
  
        if (!response.ok) {
          throw new Error("Benchmark failed")
        }
  
        const result = await response.json()
  
        // Update the table with the new benchmark results
        updateResultsTable(result)
  
        // Re-enable the button
        runButton.textContent = "Run Benchmark"
        runButton.disabled = false
      } catch (error) {
        console.error("Error running benchmark:", error)
        runButton.textContent = "Run Benchmark"
        runButton.disabled = false
        alert("Error running benchmark. Please try again.")
      }
    })
  
    function updateResultsTable(result) {
      // Add the new result to the table
      addResultRow(result)
    }
  
    function addResultRow(result) {
      const newRow = resultsTable.insertRow()
  
      // Add cells with result data
      const cpuCell = newRow.insertCell()
      cpuCell.textContent = result.cpu_model
  
      const osCell = newRow.insertCell()
      osCell.textContent = result.os_name
  
      const fileSizeCell = newRow.insertCell()
      fileSizeCell.textContent = result.file_size
  
      const encTimeCell = newRow.insertCell()
      encTimeCell.textContent = result.encryption_time + "s"
  
      const decTimeCell = newRow.insertCell()
      decTimeCell.textContent = result.decryption_time + "s"
  
      const execTimeCell = newRow.insertCell()
      execTimeCell.textContent = result.execution_time + "s"
    }
  })