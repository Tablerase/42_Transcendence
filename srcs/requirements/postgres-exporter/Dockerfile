# Use the official Golang image to build the exporter
FROM golang:1.20 as builder

# Set the working directory
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/prometheus-community/postgres_exporter.git .

# Build the exporter
RUN make build

# Use a minimal image to run the exporter
FROM alpine:latest

# Install necessary packages
RUN apk --no-cache add ca-certificates

# Copy the built binary from the builder stage
COPY --from=builder /app/postgres_exporter /usr/local/bin/postgres_exporter

# Expose the port that the exporter will run on
EXPOSE 9187

# Command to run the exporter
ENTRYPOINT ["/usr/local/bin/postgres_exporter"]