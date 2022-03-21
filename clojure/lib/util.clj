(ns util)

(use '[enum :only (zip)])

(defn untilrepeat [f [state & prev]]
  (if (= state (first prev))
      state
      (recur f (apply conj [(f state)] state prev))
      ))

; there has to be a better way to write this
(defn fargo [f0 & fns]
  (fn [a0 & args]
    (map
      #((first %) (second %))
      (zip (concat [f0] fns) (concat [a0] args))
      )))

(defn divmod [n d] [(- (/ n d) (/ (mod n d) d)) (mod n d)])

(defn modinv [r m]
  (loop [[A B t2 t3] [m (mod r m) 0 1]]
    (if (zero? B)
      (mod t2 m)
      (recur [B (mod A B) t3 (- t2 (* t3 (quot A B)))])
)))

; Kinda prefer the above form, tbh
;(defn modinv [r m]
;  (loop [A m B (mod r m) t2 0 t3 1]
;    (if (zero? B)
;      (mod t2 m)
;      (recur B (mod A B) t3 (- t2 (* t3 (quot A B))))
;)))

; ls = [[r0 m0] ... [rk mk]]
; find the value that satisfies all x = rk (mod mk)
; using the Chinese Remainder Theorem
(defn crt [ls]
  ((fn [p]
    (->> ls
         (map (fn [[r m]] (* r (/ p m) (modinv (/ p m) m))))
         (reduce +)
         (#(mod % p))
         ))
   (reduce * (map second ls))
  ))

