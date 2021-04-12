package com.app4shm.server

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.stereotype.Controller
import org.springframework.ui.Model
import org.springframework.web.bind.annotation.*

var data_stream : ArrayList<Data> = ArrayList()

@SpringBootApplication
class ServerApplication
fun main(args: Array<String>) {
    runApplication<ServerApplication>(*args)
}

fun clear() {
    data_stream = ArrayList()
}

@RestController
@RequestMapping("/data")
class DataGetter {
    @PostMapping("/reading")
    fun makeData(@RequestBody data: Array<Data>){
        for (i in data) {
            data_stream.add(i)
        }
    }
}

@Controller
class DataPusher {
    @GetMapping("/diag")
    fun pushData(@RequestParam(name = "printme", required = false, defaultValue = "") discarded : String, model : Model){
        var printme = ""
        for (i in data_stream) {
            printme += i.toString()
        }
        model.addAttribute("printme", printme)
    }
    @RequestMapping("/clear")
    fun doStuffMethod() {
        clear()
    }
}
