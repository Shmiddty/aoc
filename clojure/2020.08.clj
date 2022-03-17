(use '[io :rename {read-all-lines yummy debug dbg}])
(use '[clojure.string :only (split)])

(def inp
  (->> (yummy)
      (map #(split % #" "))
      (map (fn [v] (vector (first v) (Integer. (second v)))))
      (apply vector)
      ))

(def ops 
  {
   "acc" (fn [a [A I]] [(+ A a) (+ 1 I)]), 
   "jmp" (fn [a [A I]] [A (+ a I)]),
   "nop" (fn [a [A I]] [A (+ 1 I)]) 
   })

(defn IOPS [OPS] (map #(partial (get ops (first %)) (second %)) OPS))

(defn step [OPS [A I]] ((nth OPS I) [A I]))

(defn run [OPS [state & prev]]
  (if (>= (second state) (count OPS))
    [state 0]
    (if (< 0 (count (filter #(= (second state) (second %)) prev)))
      [(first prev) -1]
      (run OPS (apply conj [(step OPS state)] state prev))
      )))

(->> [[0 0]]
     (run (IOPS inp))
     (ffirst)
     (println)
     )

(->> inp
     (zipmap (range (count inp))) ; index the instructions (there's gotta be a better way!)
     (filter #(contains? {"jmp"0"nop"0} (first (second %)))) ; get the jmp and nop instructions
     (map (fn [[I [OP A]]] [I [(if (= "nop" OP) "jmp" "nop") A]])) ; swp jmp nop
     (map #(apply assoc inp %)) ; for each swapped inst, get the program with the swapped inst
     (map #(run (IOPS %) [[0 0]])) ; then run each updated program
     (filter #(= 0 (second %))) ; [[Accumulator OpIndex] ExitCode] get programs with ExitCode 0
     (first) ; there should only be one
     (ffirst) ; get the Accumulator value
     (println) ; ppfppfpffffftttt
     )

