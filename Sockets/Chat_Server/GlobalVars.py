#--------Commands--------#
command_symbol = "\\";
UserCommands = {"set_name": "setName", "disp_users": "users", "get_help": "help", "connect": "connect","disconnect": "disconnect", "admin": "admin"}
AdminCommands = {}
UserCommandList = [v for k,v in UserCommands.items()];
AdminCommandList = [v for k,v in AdminCommands.items()];

#--------Server Lists--------#
ClientAliases = [];
Users = {};
ServerLog = [];

#--------Misc Vars--------#
default_client_port = 5280;
server_port = 5280;
server_ip = "127.0.0.1";
client_buffer_size = 1024;
message_per_timeout_limit = 5;
admin_pw = "you_must_construct_additional_pylons";
