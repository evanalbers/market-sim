import json
import sys
import numpy as np
import os

import lxml.etree as ET
BASIC_TEMPLATE = """<Simulation start="0" duration="10000">
    
</Simulation> """

RFR = "1.005"
STEP_RATE = "1.01"
REFRESH_RATE = "2"
CAPITAL_MU = 1000000
CAPITAL_SD = 300000
SHARE_MU = 1000
SHARE_SD = 700
PAYOFF_MIN = 100
PAYOFF_MAX = 1000
RISK_COEFF_MU = 5
RISK_COEFF_SD = 0.7 
NUM_NOISY = 0
PRINT_TRADE = True


def addExchangeXMLElements(simulation_root, num_assets, num_agents):
    """ adds specified number of exchange elements to XML file, also their trade loggers """

    global PRINT_TRADE

    for num in range(num_assets):
        print(num)
        ET.SubElement(simulation_root, "ExchangeAgent")
        simulation_root[num_agents + num].set('name', "ASSET" + str(num))
        simulation_root[num_agents + num].set('algorithm', 'PureProRata')

    ET.SubElement(simulation_root, "PriceDataAgent")
    simulation_root[num_agents + num_assets].set("name", "PDA")
    simulation_root[num_agents + num_assets].set("num_assets", str(num_assets))
    simulation_root[num_agents + num_assets].set("exchange", "ASSET0")

    if PRINT_TRADE:
        for num in range(num_assets):
            ET.SubElement(simulation_root, "TradeLogAgent")
            simulation_root[num_agents + num_assets + num + 1].set('name', 'ASSET' + str(num) + "_LOGGER")
            simulation_root[num_agents + num_assets + num + 1].set('exchange', 'ASSET' + str(num))

    ET.SubElement(simulation_root, "ShockAgent")
    simulation_root[num_agents + num_assets + num_assets + 1].set('name', 'SA')
    simulation_root[num_agents + num_assets + num_assets + 1].set('exchange', 'ASSET0')

def addAgentXMLElements(simulation_root, num_agents):
    """ adds requisite number of agents to xml object """

    for num in range(num_agents):

        ET.SubElement(simulation_root, "SimpleCaseAgent")
        simulation_root[num].set('fp', "../../../../SimpleCaseAgent.py")
        simulation_root[num].set('name', "AGENT" + str(num))
        ## need to set arbitrary exchange here, their initialization code will be looking for an exchange anyway 
        simulation_root[num].set('exchange', 'ASSET1')
        simulation_root[num].set('refresh_rate', REFRESH_RATE)
        simulation_root[num].set('asset_file', "")
        simulation_root[num].set('rfr', RFR)
        simulation_root[num].set('step_rate',STEP_RATE)
        simulation_root[num].set('risk_coeff',"")

def generateAgentEndowments(simulation_root, num_agents, num_assets, asset_prices, name):
    """ generates endowments for agents, sets values, generates json files
        needs to be run after assets have been generated, asset generator will come up with initial price values
       """

    ## generating list of risk coeffs
    risk_coeffs = np.random.normal(RISK_COEFF_MU, RISK_COEFF_SD, num_agents).tolist()

    noisy_agents = np.random.choice(range(num_agents), NUM_NOISY, replace=False).tolist()
    print(noisy_agents)

    ## generating capital values, setting risk coeff, and json values for each agent
    for num in range(num_agents):
        capital = np.random.normal(CAPITAL_MU, CAPITAL_SD, 1)
        simulation_root[num].set('capital', str(capital[0]))
        simulation_root[num].set('risk_coeff', str(risk_coeffs[num]))


        ## TODO: Need to make this dynamic, want a range of beliefs, this presumes only 2 asset dictionaries
        if num in noisy_agents:
            simulation_root[num].set("asset_file", name + "Asset Dictionaries/" + " Asset Dictionary " + "1" + ".json")
        else: 
            simulation_root[num].set("asset_file", name + "Asset Dictionaries/" + " Asset Dictionary " + "0" + ".json")

        ## generate share endowments, stipulating that share count must be positive for now
        shares = np.absolute(np.random.normal(SHARE_MU, SHARE_SD, num_assets)).tolist()
        shares = [int(x) for x in shares]
        watching = []

        for asset_num in range(num_assets):
            watching.append("ASSET" + str(asset_num))

        if num in noisy_agents:
            agent_dict = {"watching" : watching, "prices" : asset_prices[0], "shares" : shares}
        else:
            agent_dict = {"watching" : watching, "prices" : asset_prices[0], "shares" : shares}

        print("AGENT ", num, agent_dict)

        if not os.path.isdir(name + " Agents"):
            os.mkdir(name + " Agents")


        ## generating json files for each agent
        with open(name + " Agents/Agent" + str(num) + ".json", 'w') as f:
            json.dump(agent_dict, f)

    
def generateAssetDictionary(name, num_assets, num_dicts):
    """ generates a series of arbitrary assets """

    assets = []

    for num in range(num_assets):
        assets.append("ASSET" + str(num))

    ## initializing variance list
    variances = []
    for i in range(num_assets):
        variances.append([])
        for j in range(num_assets):
            variances[i].append(0)

    ## generating expected prices
    exp_prices = (1.1 * np.random.randint(low=PAYOFF_MIN + num, high=PAYOFF_MAX + num, size=num_assets)).tolist()

    ## double for loop to determine variance matrix
    for i in range(num_assets):
        for j in range(num_assets): 
            if i == j:

                variances[i][j] = float(np.random.sample() * 0.5) * exp_prices[i]
            elif variances[i][j] == 0:
                cov_ij = float(np.random.sample() * 0.01) * exp_prices[i] * exp_prices[j]
                variances[i][j] = cov_ij
                variances[j][i] = cov_ij 

    initial_prices_list = []

    ## generating returns
    exp_prices = (1.1 * np.random.randint(low=PAYOFF_MIN + num, high=PAYOFF_MAX + num, size=num_assets)).tolist()

    initial_prices = []

    for asset_num in range(num_assets):
        initial_prices.append(float((1 - (np.random.random() * 0.01)) * exp_prices[asset_num]))

    initial_prices_list.append(initial_prices)

    if not os.path.isdir(name + " Asset Dictionaries"):
            os.mkdir(name + " Asset Dictionaries")

    for dict_num in range(num_dicts):        

        with open(name + " Asset Dictionaries" + "/Asset Dictionary " + str(dict_num) + ".json", "w") as f:
            asset_dict = {"assets" : assets, "exp_prices" : exp_prices, "variances" : variances}
            json.dump(asset_dict, f)

    return initial_prices_list



def generateSimulation(name, num_agents, num_assets):
    """ generates simulation XML file! """

    ##set up initial XML file object

    sim = ET.fromstring(BASIC_TEMPLATE)

    addAgentXMLElements(sim, num_agents)

    addExchangeXMLElements(sim, num_assets, num_agents)

    os.chdir(name)

    initial_prices = generateAssetDictionary(name, num_assets, 2)

    generateAgentEndowments(sim, num_agents, num_assets, initial_prices, name)

    ## currently using default length of time 

    ## save file to simulation folder to run it  

    simulation_tree = ET.ElementTree(sim)

    os.chdir("../")

    simulation_tree.write("maxe/build/TheSimulator/TheSimulator/" + name + '.xml')



def parseAgentFile(filename):

    document = ET.parse(filename)

    root = document.getroot()

    print(root.get('duration'))


def main():

    global NUM_NOISY

    simulation_name = sys.argv[1]
    number_agents = int(sys.argv[2])
    number_assets = int(sys.argv[3])
    if len(sys.argv) == 5:
        NUM_NOISY = int(sys.argv[4])

    if not os.path.exists(simulation_name):
            os.mkdir(simulation_name)

    generateSimulation(simulation_name, number_agents, number_assets)

main()
