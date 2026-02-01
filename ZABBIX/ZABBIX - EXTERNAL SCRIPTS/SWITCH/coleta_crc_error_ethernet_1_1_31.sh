#!/usr/bin/expect -f
set timeout 20
log_user 0

set host "[IP_ADDRESS]"
set user "monitoramento"
set port "5581"
set pass {$witchDell$@feweb}

spawn ssh -o StrictHostKeyChecking=accept-new -p $port $user@$host
expect {
  -re "(?i)password:" { send -- "$pass\r" }
  timeout { puts "TIMEOUT esperando password"; exit 1 }
}

expect {
  -re {#\s*$} {}
  timeout { puts "TIMEOUT esperando prompt do switch"; exit 2 }
}
send -- "show interface ethernet 1/1/31 | grep CRC\r"
expect {
  -re {([0-9]+)\s+discarded} {
    puts $expect_out(1,string)
  }
  timeout { puts "TIMEOUT esperando saída do comando"; exit 3 }
}
expect -re {#\s*$}
send -- "exit\r"
expect eof