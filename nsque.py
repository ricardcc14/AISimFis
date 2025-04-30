es = cna.CMAEvolutionStrategy(mu, sigma, {'popsize': poplength})
population = np.array(es.ask()).tolist()

while running:
    es.tell(population, [calcFitness(ind) for ind in population])
    population = np.array(es.ask().tolist)

    prev_fit = best_individual.f if(best_individual != None) else np.inf
    best_individual = es.best

    #ARREGLAT THIS
    if(abs(best_individual.f - prev.fit) < 0.0001 snf best_individual.f < 0.001):
        if(toFinish):
            print("done")
            running = False
        else:
            toFinish = True
            es = cma.CMAEvolutionStrategy(es.mean, sigma, {'popsize': popLength})
            population = np.array(es.ask().tolist())

        ax.contourf(X, Y, Z, levels=20, antialiased=True)
        ax.scatter([ind[0] for ind in population])


        #NO UTILITZAR!!!!!!!!!!!! NI es.OPTIMIZE() NI es.STOP()
        #UTILITZAR ASK I TELL

        #A LA FUNCIO DE FITNESS NO NOMES HI HA D'HAVER QUENTES PILOTES H HA SOTA SINO QUE TB SHI HA DE POSAR EL BUCLE DE LA SIMULACIO
        #BUCLE QUE PASSI 300 VEGADES
        #RETURN DEL FITNESS UN COP HAN PASSAT LES 300 vegades