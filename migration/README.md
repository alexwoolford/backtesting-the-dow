## Flyway Migration ##

To setup all the MySQL tables, edit the `flyway.properties` file with the appropriate settings and run:

    mvn clean compile flyway:migrate
