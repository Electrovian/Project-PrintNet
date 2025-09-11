plugins {
    // version alignment and plugin availability for subprojects
    id("org.springframework.boot") version "3.13.3" apply false
    id("io.spring.dependency-management") version "1.1.5" apply false
    kotlin("jvm") version "2.0.0" apply false
    kotlin("plugin.spring") version "2.0.0" apply false
}

allprojects {
    repositories {
        mavenCentral()
    }
}