import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._stato = None

    def handleCalcola(self, e):
        #ricavo l'anno dall'input dell'utente
        anno = self._view._txtAnno.value
        try:
            a = int(anno)
        except:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione devi digitare un numero intero positivo compreso tra"
                                                           "1816 e 2016"))
            self._view.update_page()
        #crea grafo
        self._model.buildGraph(a)

        self._view.update_page()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        #stampa il numero di componenti connesse
        nc = self._model.getNumCompConnesse()
        self._view._txt_result.controls.append(ft.Text(f"Il grafo a {nc} componenti connesse"))
        # il popolamento del secondo dropdown si fa chiamando nel bottone prima tale popolamento
        self.popolamento_dd_stato()
        #stampa elenco nodi/stati con il numero di rispettivi vicini
        self._view._txt_result.controls.append(ft.Text(f"Di seguito il dettaglio sui nodi:"))
        self._view.update_page()
        statiegradi=self._model.getStati()
        for s,g in statiegradi:
                self._view._txt_result.controls.append(ft.Text(f"{s.StateNme}--{g} vicini"))
                self._view.update_page()

    def popolamento_dd_stato(self):
        stati = self._model.getAllStati() #lista di oggetti di tipo stato, tutti quelli del grafo
        for s in stati:
             self._view._ddStato.options.append(ft.dropdown.Option(key=str(s.CCode),
                                                                   data=s,
                                                                   text=s.StateNme,
                                                                   on_click = self.read_stato
                                                                   ))
        self._view.update_page()
        #PER POPOLARE DEVI SCHIACCIARE CALCOLA CONFINI, PERCHE IL DROPDOWN DEVE ESSERE POPOLATO SOLO ED ESCLUSIVAMENTE CON GLI STATI CHE SONO NODI DEL GRAFO

    def read_stato(self,e):
        s = e.control.data
        if s is None:
            self._stato = None
        else:
            self._stato = s


    def handleStatiRaggiungibili(self,e):
        #visualizza la lista di tutti i nodi raggiungibili a partire da quello selezionato
        #che coincide con la comp connessa del grafo relativa allo stato scelto
        #puoi usare tre metodi diversi per visitare il grafo: BreadthFirstIterator, DeepFirstIterator di nx
        #implementando manualmente un alg ricorsivo per la visita in profondità
        #implementando manualmente alg iterativo (li faccio poi quando studio la ricorsione)

        # 1. Controllo di sicurezza: l'utente ha selezionato uno stato?
        if self._stato is None:
                self._view._txt_result.controls.clear()
                self._view._txt_result.controls.append(
                    ft.Text("Attenzione: Seleziona prima uno stato dal menù a tendina!", color="red")
                )
                self._view.update_page()
                return

        # Puliamo l'area di testo dei risultati precedenti
        self._view._txt_result.controls.clear()

        # 2. Chiamiamo il metodo del modello (usiamo quello iterativo manuale richiesto)
        # Nota: Puoi scambiarlo con self._model.get_raggiungibili_nx(self._stato) per testare l'altro!
        raggiungibili = self._model.get_raggiungibili_iterativo(self._stato)

        # Ordiniamo i risultati in ordine alfabetico per renderli eleganti a schermo
        raggiungibili.sort(key=lambda x: x.StateNme)

        # 3. Stampiamo i risultati nella ListView
        self._view._txt_result.controls.append(
                ft.Text(f"Stati raggiungibili a partire da: {self._stato.StateNme}", weight=ft.FontWeight.BOLD,
                        color="blue")
            )
        self._view._txt_result.controls.append(
                ft.Text(f"Totale stati raggiungibili: {len(raggiungibili)}")
            )

        if len(raggiungibili) == 0:
                self._view._txt_result.controls.append(
                    ft.Text("Nessuno stato raggiungibile via terra (è un'isola o non ha vicini in questo anno).")
                )
        else:
                # Ciclo per stampare i nomi di tutti gli stati trovati nella componente connessa
                for paese in raggiungibili:
                    self._view._txt_result.controls.append(ft.Text(f"- {paese.StateNme}"))

        # Aggiorniamo la pagina per mostrare i testi a schermo
        self._view.update_page()

