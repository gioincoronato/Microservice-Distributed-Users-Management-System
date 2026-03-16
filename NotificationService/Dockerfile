FROM openjdk:11-jdk-slim
WORKDIR /app
COPY . .
RUN javac -cp ".:lib/*" NotificationService.java
CMD ["java", "-cp", ".:lib/*", "NotificationService"]