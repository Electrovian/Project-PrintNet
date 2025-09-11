plugins {
    kotlin("jvm") version "2.0.0"
    application
}

group = "edu.uc.printnet.worker"
version = "0.0.1-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.jetbrains.kotlin:kotlin-stdlib")
    implementation("com.rabbitmq:amqp-client:5.21.0")
}

application {
    mainClass.set("edu.uc.printnet.worker.SlicerJobRunnerKt")
}