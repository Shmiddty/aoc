(use '[io :rename {read-all-lines yummy, printI printI}])
(use '[clojure.string :only (split)])
(use '[enum :only (enumerate)])
(use '[util :only (fargo, crt)])

(def inp
  (apply
    (fargo read-string #(split % #","))
    (yummy)
    ))

; so damn unpretty
;(->> inp
;     ((fn [[a B]]
;        (->> B
;             (filter #(not= "x" %))
;             (map read-string)
;             (map
;               (fn [b]
;                 (->> (iterate (partial + b) 0)
;                      (drop-while (partial > a))
;                      (first)
;                      (vector b)
;                 )))
;             (apply min-key second)
;             ((fn [[b t]] (* b (- t a))))
;          )
;        ))
;     (println)
;     )

; slightly less unpretty
((
  fn [[a B]] (->> B
    (filter #(not= "x" %))
    (map read-string)
    (map (fn [b] [(mod (- 0 a) b) b]))
    (apply min-key first)
    (reduce *)
    (println)
  ))
  inp
)

;(defn catchup [[one & more]]
;  (apply conj [(drop-while #(< % (first (last more))) one)] more)
;  )
;
;; still too slow... hmmmmmmm
;(defn seek [iters]
;  (if (= 1 (count (set (map first iters))))
;    (ffirst iters)
;    (recur (sort-by first (catchup iters)))
;  ))

; maybe this is actually a least common multiple problem, kinda.
; so is it better to iterate the busses like I was doing originally?
; it shouldn't be necessary to iterate *all* of them...
; will the value be less than their cumulative product?
; so maybe we can work backward from there? not sure if that'd actually be faster
; it's the chinese remainder theorem. I did this before but forgot all about it.
(->> inp
     (second)
     (enumerate)
     (filter #(not= "x" (second %)))
     (map (partial apply (fargo identity read-string)))
     (map (fn [[i d]] [(mod (- 0 i) d) d]))
     (crt)
     (println)
     ;((fn [ls]
     ;   (->> ls
     ;        (map (fn [[i d]] #(= 0 (mod (+ i %) d))))
     ;        (apply every-pred)
     ;        ; let's try to step lively
     ;        ; looks like this is still too slow.
     ;        (#(filter
     ;            %
     ;            (map
     ;              (partial + (* -1 (first (apply max-key second ls))))
     ;              (iterate (partial + (apply max (map second ls))) 0)
     ;              )))
     ;        ; this is all pretty icky, huh?
     ;        ; guess it was all a fluke, eh?
     ;        ; guess my life has no value, right?
     ;        (first)
     ;        (printI)
     ;        )))
     )
