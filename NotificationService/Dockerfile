
FROM eclipse-temurin:11-jdk

WORKDIR /app


COPY . .

RUN javac -cp ".:lib/*" NotificationService.java


CMD ["java", "-cp", ".:lib/*", "NotificationService"]
