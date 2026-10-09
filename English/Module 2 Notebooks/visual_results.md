# Visual Results

## Figure 1 — Temporal evolution of consumption (30 days)

The three sites **Industry** dominate significantly in volume (1.5 – 2.5 MW), with a regular profile and weekly cycles clearly visible:



 1 .Consumption falls systematically on weekends, a sign of industrial activity strictly set on working days.



 2.Sites **Commercial** showed a more stable behavior (~0.6 – 0.9 MW) with less variance. 



3.Sites **Resident** remain below 0.35 MW with a slight upward trend in the mid-period, probably due to weather conditions.



 **Operational conclusion**: industrial sites are the priority levers for any erasure or optimization program.

## Image 2 — Comparative KPIs (loading rate, anomalies, prediction)

Trois enseignements distincts ressortent. 

1.On the **load rate**, SITE RES 001 and SITE RES 002 have the highest rates relative to their capacity (~48%), which is counter-intuitive — due to their low installed capacity (0.6–0.8 MW) compared to constant consumption. 



2.On ** anomalies**, SITE COM 001 stands out with a rate of 1.94%, double the average — to be monitored. 



3.On the** prediction error**, industrial sites are best predicted (<20%), while SITE IND 001 has the highest value (~58%), indicating that its behaviour is less regular and that the forecasting model deserves refinement at this site.

---

## Image 3 — Price sensitivity and erasure gains

1 .The left scatter shows **no strong linear correlation** between spot price and consumption 

2. sites do not spontaneously reduce their activity when the price rises, which fully justifies the implementation of **active erasure signs**.

3. On potential earnings, SITE IND 001 represents the dominant deposit with **~100 k€** potential gain over 30 days, compared to ~69 k€ for SITE IND 002. 

4. These two flexible industrial sites concentrate 100% of the erasure potential. 



**Conclusion**: A SITE IND 001-targeted erasure program alone would make it possible to leverage most of the park's financial potential.

---

## 4 — Heatmap Time × Weekday

The heatmap reveals a very readable **consumption structure** in three zones. 

1.The 8h-19h weekday (dark red, ~1.4 MW) is the peak of industrial and commercial activity. 

2.The night (0h–6h) and weekends (light orange, ~0.6–0.8 MW) represent the hollows — ideal for maintenance or charging operations. 

3 There is a **light asymmetry**: Friday evening picks up earlier than the other working days, and Saturday morning maintains a residual activity until 10am. 



These patterns can be used directly to configure **automatic erasure extensions** in the monitoring system.

---

## Image 5 — Operational alerts and anomalies

The left graph shows that **"Very high spot prices"** generate by far the largest volume of alerts (mostly HIGH priority), in front of prediction errors (MOYENNE) and abnormal consumptions (HAute/CRITICAL mix).

 The right timeline confirms that critical alerts focus on **two distinct periods** within the month — point price peaks likely related to network tensions. 

The absence of CRITICAL alerts outside these windows is reassuring: the park normally operates 90% of the time. **Recommended action**: set automatic notifications on historically identified risk slots on the timeline.
