# Load the necessary package
library(ggplot2)

# Read command-line arguments for the output file name
args <- commandArgs(trailingOnly = TRUE)
output_file <- ifelse(length(args) >= 1, args[1], "output.png")  # Default to "output.png" if not provided

# Read the data from standard input
data <- read.table(file("stdin"), header = TRUE, sep = "\t")


print(colnames(data))


# Create the plot and store it in an object
p <- ggplot(data, aes(x = Sample.Type, y = new_TPM)) +
     geom_boxplot(notch = TRUE) +
     geom_jitter(width = 0.2, color = "blue", size = 2, alpha = 0.6) +
     labs(title = "Lung Adenocarcinoma", x = "Tumor Type", y = "log2(TPM+1)") +
     theme_minimal()

# Save the plot as specified by the output filename
ggsave(output_file, plot = p, width = 8, height = 6)

