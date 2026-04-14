# Use Node image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all frontend code
COPY . .

# Build Next.js app
RUN npm run build

# Expose port
EXPOSE 3000

# Start app
CMD ["npm", "start"]