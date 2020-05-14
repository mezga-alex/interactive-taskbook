// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

const defaultBackgroundColor = ['#e74a3b', '#1cc88a'];
const defaultHoverBackgroundColor = ['#a83f30', '#17a673'];
const defaultHoverBorderColor = "rgba(234, 236, 244, 1)";
const defaultLabels = ["Wrong Answers", "Correct Answers"];
const defaultOptions = {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    };

// Create a structure from raw data
function createDataStructure(dataValues, labels=defaultLabels, backgroundColor=defaultBackgroundColor,
                             hoverBackgroundColor=defaultHoverBackgroundColor, hoverBorderColor=defaultHoverBorderColor) {
    return  {
        labels: labels,
        datasets: [{
            data: dataValues,
            backgroundColor: backgroundColor,
            hoverBackgroundColor: hoverBackgroundColor,
            hoverBorderColor: hoverBorderColor,
        }],
    };
}

// Compile the data into a Pie Chart
function createPieChart(dataValues, elementID="myPieChart",
                        labels=defaultLabels, options=defaultOptions) {

    const data = createDataStructure(dataValues, labels);
    // Pie Chart
    var ctx = document.getElementById(elementID);
    var myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: options,
    });
}
