welcome_text = f"I am a bot that will help create and manage your tokenized community.\n\n" + \
               "That\'s what I can do:\n\n" + \
               "/create_community_with_token - creating a community and token. Token will have the name, symbol, and minting price you specified in arguments." \
               " Payment for the token issue will be sent to the community wallet address you specified. [only Direct Messages with bot]\n" \
               "<b>Arguments: Name Symbol Price community_wallet</b>\n" + \
               "Example: <code>/create_community_with_token MyTokenName MTN 0.05 0x0000000000000000000000000000000000000000</code>\n\n" + \
               "/create_community_custom_token - creating a community with the token address you specified in arguments.[DM]\n" \
               "Please, note that some features may work differently with custom token implementations.\n" \
               "<b>Arguments: community_wallet community_token</b>\n" + \
               "Example: <code>/create_community_custom_token 0x00000000000000000000000000000000000000000 0x1111111111111111111111111111111111111111</code>\n\n" + \
               "/mint_tokens - mint your community token in exchange for a native network token (ETH). [DM]" \
               "<b>Arguments: token_address integer_amount\n</b>" + \
               "Example: <code>/mint_tokens 0x0000000000000000000000000000000000000000 1</code>\n\n" + \
               "/change_token_price - changing the exchange rate of your token." \
               " This method is only available to the community wallet or owner. [DM]\n" + \
               "<b>Arguments: token_address new_price</b>\n" + \
               "Example: <code>/change_token_price 0x0000000000000000000000000000000000000000 0.07</code>\n\n" + \
               "/add_community_token - setting a community token for a chat. [Group Chat only]\n" + \
               "<b>Arguments: token_address </b>\n" + \
               "Example: <code>/add_community_token 0x0000000000000000000000000000000000000000</code>\n\n" + \
               "/get_community_token_address - will remind you of the community token address set in this chat." \
               "[GC]\n<b>No arguments</b>\n\n" + \
               "/delete_community_token - remove the community token for this chat. [GC]\n<b>No arguments</b>\n\n" + \
               "/join_group - sending a personal link to join a community chat after passing a community token balance check. [DM]\n" + \
               "<b>Arguments: community_token</b>\n" + \
               "Example: <code>/join_group 0x0000000000000000000000000000000000000000</code>\n\n" + \
               "/get_mint_deeplink - create an invite deeplink to mint the community token.[GC]\n" + \
               "<b>Arguments: amount</b>\n" + \
               "Example: <code>/get_mint_deeplink 2</code>\n\n" + \
               "/get_join_deeplink - create an invite deeplink to join the community chat. [GC]\n\<b>No arguments</b>\n\n" + \
               "/verify_member - use this command to verify new member of community. [DM]\n" + \
               "<b>Arguments: token_address member_id</b>\n" + \
               "Example: <code>/verify_member 0x0000000000000000000000000000000000000000 191034810</code>\n\n" \
               "/create_task - create a task for community. The deadline parameter should be an integer number of hours" \
               " allocated for providing solutions. Reward in ETH. [GC]\n" + \
               "<b>Arguments: deadline reward</b>\n" + \
               "Example: <code>/create_task 1 1</code>\n\n" + \
               "/create_voting - create a voting. The deadline parameter should be an integer number of hours" \
               " allocated for providing votes.[GC]\n" + \
               "<b>Arguments: number_of_options deadline</b>\n" + \
               "Example: <code>/create_voting 2 1</code>\n\n" + \
               "/propose_solution - propose solution to the task. [GC]\n" + \
               "<b>Arguments: task_id</b>\n" + \
               "Example: <code>/propose_solution 42</code>\n\n" + \
               "/start_voting_on_solutions - start voting for the best solution of the task. [GC]\n" + \
               "<b>Arguments: task_id deadline</b>\n" + \
               "Example: <code>/start_voting_on_solutions 6 7</code>\n\n" + \
               "/vote - vote for an option. [DM]\n" + \
               "<b>Arguments: community_token voting_id deadline</b>\n" + \
               "Example: <code>/vote 0x0000000000000000000000000000000000000000 6 7</code>\n\n" + \
               "/get_voting - sends information about the voting. [GC]\n" + \
               "<b>Arguments: voting_id</b>\n" + \
               "Example: <code>/get_voting 7</code>\n\n" + \
               "/get_task - sends information about the task. [GC]\n" + \
               "<b>Arguments: task_id</b>\n" + \
               "Example: <code>/get_task 0</code>\n\n" + \
               "/get_solution - sends information about the task's solution. [GC]\n" + \
               "<b>Arguments: task_id sol_id</b>\n" + \
               "Example: <code>/get_solution 0 1</code>\n\n" + \
                "/count_voting_results - sums up the voting results.[GC]\n" + \
               "<b>Arguments: voting_id</b>\n" + \
               "Example: <code>/count_voting_results 0</code>\n\n" + \
               "/count_task_voting_results - sums up the results of voting for the best solution to the task.[GC]\n" + \
               "<b>Arguments: task_id</b>\n" + \
               "Example: <code>/count_task_voting_results 0</code>\n\n" + \
               "/reward_solvers - use it to send reward to the creator(s) of the winning solution(s) of the task.[GC]\n" + \
               "<b>Arguments: task_id</b>\n" + \
               "Example: <code>/reward_solvers 0</code>\n\n" + \
               "/help or /start - send this message"
