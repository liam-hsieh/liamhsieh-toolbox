## Metaheuristic

to be continued..


Example of flowchart using mermaid.
This will be applied for providing a high-level explanation for optimization algorithms in this module.

```mermaid
flowchart LR;
  Start[Start:<br>pass run_id and trigger <br>targeted procedure]-->|run_id| Proc[Procedure] 
  Proc-->check{Do db <br>files exist?}
  check-->|no| End[throw exception]
  check-->|yes: scen files| mf[Model Feeder:<br>pass and cache model_feed]
  mf-->|model feed:<br>*IDXSET<br>*SET<br>*PARAM<br>*INFO<br>*COEF<br>*VAR<br>|M3[Optimization model:<br>cache model files]
  M3-->M4[Export results]
```

> **Warning**
> This is warning
