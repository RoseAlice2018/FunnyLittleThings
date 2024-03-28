// script.js
function calculateFinalValue() {
    var workHours = parseInt(document.getElementById("workHours").value);
    var workHoursCoefficient = parseInt(document.getElementById("workHoursCoefficient").value);
    var workEnvironment = parseInt(document.getElementById("workEnvironment").value);
    var workEnvironmentCoefficient = parseInt(document.getElementById("workEnvironmentCoefficient").value);
    var jobProspects = parseInt(document.getElementById("jobProspects").value);
    var jobProspectsCoefficient = parseInt(document.getElementById("jobProspectsCoefficient").value);
    var salary = parseInt(document.getElementById("salary").value);
    var salaryCoefficient = parseInt(document.getElementById("salaryCoefficient").value);
    var jobCost = parseInt(document.getElementById("jobCost").value);
    var jobCostCoefficient = parseInt(document.getElementById("jobCostCoefficient").value);
  
    var finalValue = workHours * workHoursCoefficient + workEnvironment * workEnvironmentCoefficient + jobProspects * jobProspectsCoefficient + salary * salaryCoefficient + jobCost * jobCostCoefficient;
    document.getElementById("finalValue").innerHTML = finalValue;
  }
  
  document.getElementById("workHours").addEventListener("change", calculateFinalValue);
  document.getElementById("workHoursCoefficient").addEventListener("change", calculateFinalValue);
  document.getElementById("workEnvironment").addEventListener("change", calculateFinalValue);
  document.getElementById("workEnvironmentCoefficient").addEventListener("change", calculateFinalValue);
  document.getElementById("jobProspects").addEventListener("change", calculateFinalValue);
  document.getElementById("jobProspectsCoefficient").addEventListener("change", calculateFinalValue);
  document.getElementById("salary").addEventListener("change", calculateFinalValue);
  document.getElementById("salaryCoefficient").addEventListener("change", calculateFinalValue);
  document.getElementById("jobCost").addEventListener("change", calculateFinalValue);
  document.getElementById("jobCostCoefficient").addEventListener("change", calculateFinalValue);