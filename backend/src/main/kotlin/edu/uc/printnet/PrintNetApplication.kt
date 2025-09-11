package edu.uc.printnet

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class PrintNetApplication

fun main(args: Array<String>) {
    runApplication<PrintNetApplication>(*args)
}
