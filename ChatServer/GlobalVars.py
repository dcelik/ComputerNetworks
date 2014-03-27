from MAC_Identifier import my_ad

#--------Commands--------#
command_symbol = "/";

#--------Server Lists--------#
Users = {};
IPs = {};
ServerLog = [];
BannedIPs=[];

#--------Misc Vars--------#
default_client_port = "";
server_port = "";
server_ip = my_ad;
client_buffer_size = 1024;
message_per_timeout_limit = 5;
admin_pw = "nick";
