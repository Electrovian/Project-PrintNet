package edu.uc.printnet

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@SpringBootApplication
class PrintNetApplication

fun main(args: Array<String>) {
    runApplication<PrintNetApplication>(*args)
}

@RestController
class HealthController {
    @GetMapping("/api/health")
    fun health() = mapOf("status" to "ok")
}