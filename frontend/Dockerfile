# Step 1: Use the official Node.js image
FROM node:16

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install dependencies
COPY package.json package-lock.json /app/
RUN npm install

# Step 4: Copy the frontend code to the container
COPY ./src /app/src
COPY ./public /app/public

# Step 5: Build the React app
RUN npm run build

# Step 6: Install a simple server to serve the build
RUN npm install -g serve

# Step 7: Expose the port React app will run on
EXPOSE 5000

# Step 8: Command to serve the React app
CMD ["serve", "-s", "build", "-l", "5000"]
