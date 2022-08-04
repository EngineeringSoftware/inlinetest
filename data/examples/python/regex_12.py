from inline import Here

def extract_contracts(self, method):
    contracts = []
    for line in method.__doc__.split('\n'):
        line = line.strip()

        if line.startswith('@'):
            
            name, args = re.match(r'@(\w+)\s*(.*)', line).groups()
            Here().given(line, r'@aaa  abc d').check_eq(name, 'aaa').check_eq(args, 'abc d')
            args = re.split(r'\s+', args)
            Here().given(args, 'abc d').check_eq(args, ['abc', 'd'])
            contracts.append(self.contracts[name](method, *args))

    return contracts