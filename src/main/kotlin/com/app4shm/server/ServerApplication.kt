package com.app4shm.server

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.stereotype.Controller
import org.springframework.ui.Model
import org.springframework.web.bind.annotation.*

var printme : String = ""
val LINENUMBER = 500

@SpringBootApplication
class ServerApplication
fun main(args: Array<String>) {
    runApplication<ServerApplication>(*args)
}

fun getHtmlLines() : Int {
    var count = 0
    for (char in printme) {
        if (char == '\n') {
            count++
        }
    }
    return count
}

@RestController
@RequestMapping("/data")
class DataGetter {
    @PostMapping("/reading")
    fun makeData(@RequestBody data: Array<Data>){
        for (i in data) {
            printme += i.toString()
            print(i.toString());
            if (getHtmlLines() > LINENUMBER) {
                printme = ""
            }
        }
    }
}

@Controller
class DataPusher {
    @GetMapping("/diag")
    fun pushData(@RequestParam(name = "printme", required = false, defaultValue = "") discarded : String, model : Model){
        var printing_str : String = printme
        printing_str = printing_str.replace("\n", "'<br>'")
        model.addAttribute("printme", printme)
    }
}