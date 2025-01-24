# Use the official Node.js image from the Docker Hub
FROM node:22

# Set the working directory in the container
WORKDIR /CONTAINER

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install the application dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port the application will run on
EXPOSE 3000

# Define the command to run the application
CMD ["cd", "vite-project", "npm", "run" "dev"]